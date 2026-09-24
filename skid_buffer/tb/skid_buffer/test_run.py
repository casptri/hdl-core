#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _runner import run_cocotb


def test_run():
    run_cocotb(
        sources=["skid_buffer/hdl/skid_buffer.vhd"],
        hdl_toplevel="skid_buffer",
        test_module="skid_buffer_tb",
        caller_file=__file__,
    )


if __name__ == "__main__":
    test_run()
