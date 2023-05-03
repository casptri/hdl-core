#/usr/bin/env python3
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from cocotb.triggers import RisingEdge
from cocotb.triggers import Timer
from cocotb.triggers import ClockCycles
import numpy as np
import random
from ecc import ECC

ecc = ECC()

CLK_PERIOD_NS=10

def setup_dut(dut):
    cocotb.fork(Clock(dut.clk, CLK_PERIOD_NS, units='ns').start())
    dut.rst <= 1
    dut._log.debug("Resetting DUT")

#@cocotb.test()
#async def rth_parity(dut):
#    test_data = random.randint(0,2**39-1)
#    dut.data.value <= test_data
#    r = dut.C_RTH.value
#    soll = ecc.calcParityOfR(test_data,r)
#    await Timer(CLK_PERIOD_NS * 10, units='ns')
#    ist = dut.parity.value
#    assert ist == soll, "Wrong parity: got {}, expected {}".format(ist,soll)

#@cocotb.test()
#async def ecc_decode(dut):
#    setup_dut(dut)
#    dut.in_valid <= 0
#    dut.in_data <= 0
#    dut.out_ready <= 0
#    await Timer(CLK_PERIOD_NS * 10, units='ns')
#    dut.rst <= 0
#    await Timer(CLK_PERIOD_NS * 10, units='ns')
#    data = random.randint(0,2**32-1)
#    encoded_data = ecc.encode(data)
#    error = 1 << random.randint(0,39)
#    error |= random.randint(0,1) << random.randint(0,39)
#    #error = 1 << 3
#    encoded_data ^= error
#    par,pos = ecc.decode(encoded_data)
#    print("parity:",par,"postition:",pos)
#    dut.in_data <= encoded_data 
#    dut.in_valid <= 1
#    dut.out_ready <= 1
#    await Timer(CLK_PERIOD_NS * 10, units='ns')
#    ist_par = dut.out_is_err.value
#    ist_value = dut.out_data.value
#    print("parity hw:",ist_par)
#    if par:
#        print("correct value")
#        assert ist_value == data, "Wrong result: got {}, expected {}".format(ist_value,bin(data))
#    else:
#        print("error detected")
#        assert ist_par == par^1, "Wrong result: got {}, expected {}".format(ist_pos,pos)

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
    assert ist_data == encoded_data, "Wrong result: got\n {}, expected\n {}".format(ist_data,bin(encoded_data))

