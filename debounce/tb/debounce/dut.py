import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer


class DutWrapper:
    def __init__(self, dut, clock_period):
        self.dut = dut
        self.clkPeriod = clock_period
        clock = Clock(dut.clk, self.clkPeriod, unit="ns")
        cocotb.start_soon(clock.start(start_high=False))
        self.dut.rst.value = 1
        self.dut.sig_in.value = 0

    async def reset(self):
        self.dut.rst.value = 1
        await Timer(100 * self.clkPeriod, unit="ns")
        self.dut.rst.value = 0
