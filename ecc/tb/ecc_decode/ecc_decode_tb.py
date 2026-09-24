import random
import sys
from pathlib import Path

import cocotb
from cocotb.triggers import FallingEdge, ReadOnly, RisingEdge, Timer

from dut import DutWrapper

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
from ecc import ECC

ecc = ECC()

CLK_PERIOD_NS = 10
ENCODED_WIDTH = ecc.b  # data + Hamming parity + overall parity bit


@cocotb.test()
async def ecc_decode(dut):
    tb = DutWrapper(dut, CLK_PERIOD_NS)
    dut.in_valid.value = 0
    dut.in_data.value = 0
    dut.out_ready.value = 0
    await tb.reset()
    data = random.randint(0, 2**32 - 1)
    encoded_data = ecc.encode(data)
    error = 1 << random.randint(0, 39)
    error |= random.randint(0, 1) << random.randint(0, 39)
    encoded_data ^= error
    par, pos = ecc.decode(encoded_data)
    print("parity:", par, "position:", pos)
    dut.in_data.value = encoded_data
    dut.in_valid.value = 1
    dut.out_ready.value = 1
    await Timer(CLK_PERIOD_NS * 10, unit="ns")
    ist_par = int(dut.out_is_err.value)
    ist_value = int(dut.out_data.value)
    print("parity hw:", ist_par)
    if par:
        print("correct value")
        assert ist_value == data, f"Wrong result: got {ist_value}, expected {bin(data)}"
    else:
        print("error detected")
        assert ist_par == par ^ 1, f"Wrong result: got {ist_par}, expected {par}"


def _make_transaction():
    """Build one stimulus: (received_word, expected_data, expected_is_err).

    Injects 0, 1 or 2 (distinct) bit errors. For 0/1 errors the data is
    recoverable; 2 errors are an uncorrectable double error (out_is_err = 1).
    ``expected_data`` is only meaningful when ``expected_is_err`` is 0.
    """
    data = random.randint(0, 2**32 - 1)
    word = ecc.encode(data)
    n_err = random.choice([0, 1, 1, 2])
    for pos in random.sample(range(ENCODED_WIDTH), n_err):
        word ^= 1 << pos
    par, syndrome = ecc.decode(word)
    is_err = 1 if (syndrome != 0 and par == 0) else 0
    return word, data, is_err


async def _drive_stream(dut, words):
    """Drive encoded words on the input handshake, honouring in_ready."""
    dut.in_valid.value = 0
    for word in words:
        await FallingEdge(dut.clk)
        dut.in_data.value = word
        dut.in_valid.value = 1
        while True:
            await ReadOnly()
            accepted = int(dut.in_ready.value) == 1
            await RisingEdge(dut.clk)
            if accepted:
                break
            # Re-sync to the falling edge before re-sampling in_ready so that
            # out_ready (driven on falling edges) is settled for the new cycle.
            await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.in_valid.value = 0


async def _monitor_stream(dut, captured, count):
    """Capture (out_data, out_is_err) on every accepted output beat.

    Sampling happens after the falling edge so that out_data, out_valid and
    out_ready all reflect the same cycle (out_ready is driven on falling edges).
    A beat sampled here with valid & ready is the one consumed at the next
    rising edge.
    """
    while len(captured) < count:
        await FallingEdge(dut.clk)
        await ReadOnly()
        if int(dut.out_valid.value) == 1 and int(dut.out_ready.value) == 1:
            captured.append((int(dut.out_data.value), int(dut.out_is_err.value)))


async def _random_backpressure(dut):
    """Randomly assert/deassert out_ready to stress the handshake."""
    while True:
        await FallingEdge(dut.clk)
        dut.out_ready.value = 1 if random.random() < 0.6 else 0


def _check(expected, captured):
    for i, ((exp_data, exp_err), (got_data, got_err)) in enumerate(
        zip(expected, captured)
    ):
        assert got_err == exp_err, f"beat {i}: out_is_err={got_err}, expected {exp_err}"
        if exp_err == 0:
            assert got_data == exp_data, (
                f"beat {i}: out_data={got_data:#x}, expected {exp_data:#x}"
            )


@cocotb.test(timeout_time=500, timeout_unit="us")
async def ecc_decode_stream(dut):
    """Stream words back-to-back; out_is_err must stay aligned with out_data."""
    random.seed(1)
    tb = DutWrapper(dut, CLK_PERIOD_NS)
    dut.in_valid.value = 0
    dut.in_data.value = 0
    dut.out_ready.value = 1
    await tb.reset()

    count = 64
    transactions = [_make_transaction() for _ in range(count)]
    words = [t[0] for t in transactions]
    expected = [(t[1], t[2]) for t in transactions]

    captured = []
    cocotb.start_soon(_monitor_stream(dut, captured, count))
    await _drive_stream(dut, words)

    for _ in range(200):
        if len(captured) >= count:
            break
        await RisingEdge(dut.clk)

    assert len(captured) == count, f"captured {len(captured)} of {count} outputs"
    _check(expected, captured)


@cocotb.test(timeout_time=500, timeout_unit="us")
async def ecc_decode_backpressure(dut):
    """Same alignment check under randomized downstream backpressure."""
    random.seed(2)
    tb = DutWrapper(dut, CLK_PERIOD_NS)
    dut.in_valid.value = 0
    dut.in_data.value = 0
    dut.out_ready.value = 0
    await tb.reset()

    count = 64
    transactions = [_make_transaction() for _ in range(count)]
    words = [t[0] for t in transactions]
    expected = [(t[1], t[2]) for t in transactions]

    captured = []
    cocotb.start_soon(_random_backpressure(dut))
    cocotb.start_soon(_monitor_stream(dut, captured, count))
    await _drive_stream(dut, words)

    for _ in range(500):
        if len(captured) >= count:
            break
        await RisingEdge(dut.clk)

    assert len(captured) == count, f"captured {len(captured)} of {count} outputs"
    _check(expected, captured)
