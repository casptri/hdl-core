#/usr/bin/env python3
import cocotb
from cocotb.triggers import Timer
import random
import sys

sys.path.append("../utils")
from ecc import ECC

ecc = ECC()

@cocotb.test()
async def rth_parity(dut):
    for _ in range(1000):
        test_data = random.randint(0,2**39-1)
        dut.data.value = test_data
        r = dut.C_RTH.value
        soll = ecc.calcParityOfR(test_data, r)
        await Timer(100, units='ns')
        ist = dut.parity.value
        assert ist == soll, "Wrong parity: got {}, expected {}".format(ist, soll)
