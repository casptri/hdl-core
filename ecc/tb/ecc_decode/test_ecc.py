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
async def ecc_decode(dut):
    setup_dut(dut)
    dut.in_valid <= 0
    dut.in_data <= 0
    dut.out_ready <= 0
    await Timer(CLK_PERIOD_NS * 10, units='ns')
    dut.rst <= 0
    await Timer(CLK_PERIOD_NS * 10, units='ns')
    data = random.randint(0,2**32-1)
    encoded_data = ecc.encode(data)
    error = 1 << random.randint(0,39)
    error |= random.randint(0,1) << random.randint(0,39)
    encoded_data ^= error
    par,pos = ecc.decode(encoded_data)
    print("parity:",par,"postition:",pos)
    dut.in_data <= encoded_data 
    dut.in_valid <= 1
    dut.out_ready <= 1
    await Timer(CLK_PERIOD_NS * 10, units='ns')
    ist_par = dut.out_is_err.value
    ist_value = dut.out_data.value
    print("parity hw:",ist_par)
    if par:
        print("correct value")
        assert ist_value == data, "Wrong result: got {}, expected {}".format(ist_value, bin(data))
    else:
        print("error detected")
        assert ist_par == par^1, "Wrong result: got {}, expected {}".format(ist_par, par)

