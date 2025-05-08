#/usr/bin/env python3
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer
import random
import sys

sys.path.append("../utils")
from ecc import ECC

ecc = ECC()

CLK_PERIOD_NS=10

def setup_dut(dut):
    cocotb.fork(Clock(dut.clk, CLK_PERIOD_NS, units='ns').start())
    dut.rst <= 1
    dut._log.debug("Resetting DUT")

@cocotb.test()
async def ecc_encode(dut):
    setup_dut(dut)
    dut.in_valid.value = 0
    dut.in_data.value = 0
    dut.out_ready.value = 0
    await Timer(CLK_PERIOD_NS * 10, units='ns')
    dut.rst.value = 0
    await Timer(CLK_PERIOD_NS * 10, units='ns')
    data = random.randint(0,2**32-1)
    encoded_data = ecc.encode(data)
    dut.in_data.value = data
    dut.in_valid.value = 1
    dut.out_ready.value = 1
    await Timer(CLK_PERIOD_NS * 10, units='ns')
    ist_data = dut.out_data.value
    print("python:",bin(encoded_data))
    print("vhdl:  ",bin(ist_data))
    assert ist_data == encoded_data, "Wrong result: got\n {}, expected\n {}".format(ist_data, bin(encoded_data))

