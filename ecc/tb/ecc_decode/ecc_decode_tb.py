import random
import sys
from pathlib import Path

import cocotb
from cocotb.triggers import Timer

from dut import DutWrapper

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
from ecc import ECC

ecc = ECC()

CLK_PERIOD_NS = 10


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
    print("parity:", par, "postition:", pos)
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
