#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _runner import run_cocotb


def test_run():
    run_cocotb(
        sources=["debounce/hdl/debounce.vhd"],
        hdl_toplevel="debounce",
        test_module="debounce_tb",
        caller_file=__file__,
    )


if __name__ == "__main__":
    test_run()
