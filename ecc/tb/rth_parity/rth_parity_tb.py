import random
import sys
from pathlib import Path

import cocotb
from cocotb.triggers import Timer

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
from ecc import ECC

ecc = ECC()


@cocotb.test()
async def rth_parity(dut):
    for _ in range(1000):
        test_data = random.randint(0, 2**39 - 1)
        dut.data.value = test_data
        r = int(dut.C_RTH.value)
        soll = ecc.calcParityOfR(test_data, r)
        await Timer(100, unit="ns")
        ist = int(dut.parity.value)
        assert ist == soll, "Wrong parity: got {}, expected {}".format(ist, soll)
