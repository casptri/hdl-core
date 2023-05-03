#-------------------------------------------------------
# test_debounce.py - tb for debouncing core
#-------------------------------------------------------
# Author: Caspar Trittibach <ctrittibach@gmail.com>
# Copyright (c) 2021 Caspar Trittibach
#-------------------------------------------------------
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge,RisingEdge
from cocotb.triggers import Timer
from cocotb.triggers import ClockCycles

CLK_PERIOD_NS = 10

def setup_dut(dut):
    cocotb.fork(Clock(dut.clk, CLK_PERIOD_NS, units='ns').start())
    dut.rst <= 1
    dut.sig_in <= 0

@cocotb.test()
async def debounce_test(dut):
    setup_dut(dut)
    deb_time = dut.DEBOUNCE_TIME.value
    print ("debounce time is:", deb_time)
    await Timer(100*CLK_PERIOD_NS,units='ns')
    dut.rst <= 0
    assert dut.sig_out.value == 0
    await FallingEdge(dut.clk)
    dut.sig_in <= 1
    await Timer((deb_time)*CLK_PERIOD_NS,units='ns')
    assert dut.sig_out.value == 0
    await Timer(3*CLK_PERIOD_NS,units='ns')
    assert dut.sig_out.value == 1, "Mismatch detected: got {}, expected 1".format(dut.sig_out.value)
