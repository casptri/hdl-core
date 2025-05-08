import cocotb
from cocotb.clock import Clock, Timer
from cocotbext.axi import (
    AxiStreamBus,
    AxiStreamSink,
    AxiStreamSource,
)


class DutWrapper:
    def __init__(self, dut, clock_period):
        self.dut = dut
        self.clkPeriod = clock_period
        clock = Clock(dut.clk, self.clkPeriod, units="ns")
        cocotb.start_soon(clock.start(start_high=False))
        self.dut.rst.value = 1

    def setup_axistream(self):
        m_bus = AxiStreamBus.from_prefix(self.dut, "m")
        self.sink = AxiStreamSink(m_bus, self.dut.clk, self.dut.rst)

        s_bus = AxiStreamBus.from_prefix(self.dut, "s")
        self.source = AxiStreamSource(s_bus, self.dut.clk, self.dut.rst)

    async def reset(self):
        self.dut.rst.value = 1
        await Timer(1, units="us")
        self.dut.rst.value = 0
