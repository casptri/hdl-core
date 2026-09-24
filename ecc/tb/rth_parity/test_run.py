#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _runner import run_cocotb


def test_run():
    run_cocotb(
        sources=["ecc/hdl/rth_parity.vhd"],
        hdl_toplevel="rth_parity",
        test_module="rth_parity_tb",
        caller_file=__file__,
    )


if __name__ == "__main__":
    test_run()
