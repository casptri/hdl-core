#!/usr/bin/env python3
import os
from pathlib import Path

from cocotb_test.simulator import run

simulator = "ghdl"
vhdl_version = "08"

tests_dir = os.path.dirname(__file__)
base_dir = Path(__file__).parents[1]
os.environ["SIM"] = os.getenv("SIM", simulator)
os.environ["COCOTB_ANSI_OUTPUT"] = "1"

file_list = [
    "hdl/skid_buffer.vhd",
]
vhdl_sources = []
for f in file_list:
    vhdl_sources.append(os.path.join(base_dir, f))


def test_run():
    run(
        vhdl_sources=vhdl_sources,
        toplevel="skid_buffer",
        module="skid_buffer_tb",
        toplevel_lang="vhdl",
        compile_args=["--std={}".format(vhdl_version), "-frelaxed-rules"],
        sim_args=["--ieee-asserts=disable-at-0"],
        waves=True,
    )


if __name__ == "__main__":
    test_run()
