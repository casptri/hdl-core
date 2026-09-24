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
async def ecc_encode(dut):
    tb = DutWrapper(dut, CLK_PERIOD_NS)
    dut.in_valid.value = 0
    dut.in_data.value = 0
    dut.out_ready.value = 0
    await tb.reset()
    data = random.randint(0, 2**32 - 1)
    encoded_data = ecc.encode(data)
    dut.in_data.value = data
    dut.in_valid.value = 1
    dut.out_ready.value = 1
    await Timer(CLK_PERIOD_NS * 10, unit="ns")
    ist_data = int(dut.out_data.value)
    print("python:", bin(encoded_data))
    print("vhdl:  ", bin(ist_data))
    assert ist_data == encoded_data, "Wrong result: got\n {}, expected\n {}".format(
        ist_data, bin(encoded_data)
    )
