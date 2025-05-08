import random

import cocotb
from cocotb.clock import Timer
from cocotb.triggers import FallingEdge

from dut import DutWrapper


@cocotb.test(timeout_time=5, timeout_unit="us", skip=False)
async def test_buffer(dut):
    """Test with cocotb axi-stream"""

    random.seed(40)

    tb = DutWrapper(dut, 10)
    tb.setup_axistream()
    await tb.reset()

    await FallingEdge(dut.clk)
    await Timer(1, units="us")
    for _ in range(10):
        val = random.randint(0, 255)
        send_transaction = tb.source.send(val.to_bytes(1, "big"))
        await send_transaction
        data = await tb.sink.read(1)
        assert val == data[0], f"{val} is not {data}"


@cocotb.test(timeout_time=5, timeout_unit="us", skip=False)
async def test_full_thruput(dut):
    """Test full thruput"""

    random.seed(40)

    tb = DutWrapper(dut, 10)
    await tb.reset()

    await FallingEdge(dut.clk)
    await Timer(1, units="us")

    await FallingEdge(dut.clk)
    for _ in range(10):
        val = random.randint(0, 255)
        assert tb.dut.s_tready.value == 1
        tb.dut.m_tready.value = 1
        tb.dut.s_tdata.value = val
        tb.dut.s_tvalid.value = 1
        await FallingEdge(dut.clk)
        assert tb.dut.m_tdata.value == val


@cocotb.test(timeout_time=5, timeout_unit="us", skip=False)
async def test_stall(dut):
    """Test stall signal"""

    random.seed(40)

    tb = DutWrapper(dut, 10)
    tb.dut.s_tdata.value = 0
    tb.dut.s_tvalid.value = 0
    tb.dut.m_tready.value = 0
    await tb.reset()

    await FallingEdge(dut.clk)
    await Timer(1, units="us")

    await FallingEdge(dut.clk)
    input_value = []
    output_value = []
    tb.dut.s_tvalid.value = 1
    tb.dut.m_tready.value = 0

    def check_and_set():
        if tb.dut.s_tready.value == 1:
            input_value.append(random.randint(0, 255))
            tb.dut.s_tdata.value = input_value[-1]

    assert tb.dut.s_tready.value == 1
    check_and_set()
    await FallingEdge(dut.clk)
    for _ in range(10):
        assert tb.dut.s_tready.value == 1
        check_and_set()
        for _ in range(3):
            await FallingEdge(dut.clk)
            assert tb.dut.s_tready.value == 0
        tb.dut.m_tready.value = 1
        check_and_set()
        output_value.append(int(tb.dut.m_tdata.value))
        assert output_value[-1] == input_value[len(output_value) - 1]
        await FallingEdge(dut.clk)
        tb.dut.m_tready.value = 0
