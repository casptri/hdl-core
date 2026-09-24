import cocotb
from cocotb.triggers import FallingEdge, Timer

from dut import DutWrapper

CLK_PERIOD_NS = 10


@cocotb.test()
async def debounce_test(dut):
    tb = DutWrapper(dut, CLK_PERIOD_NS)
    deb_time = int(dut.DEBOUNCE_TIME.value)
    print("debounce time is:", deb_time)
    await tb.reset()
    assert int(dut.sig_out.value) == 0
    await FallingEdge(dut.clk)
    dut.sig_in.value = 1
    await Timer(deb_time * CLK_PERIOD_NS, unit="ns")
    assert int(dut.sig_out.value) == 0
    await Timer(3 * CLK_PERIOD_NS, unit="ns")
    assert int(dut.sig_out.value) == 1, "Mismatch detected: got {}, expected 1".format(
        int(dut.sig_out.value)
    )
