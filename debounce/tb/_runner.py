#!/usr/bin/env python3
"""Shared cocotb runner for the debounce testbenches.

Each ``tb/<module>/test_run.py`` only declares *what* to simulate (sources,
toplevel and test module); this module holds *how* it is built and run.
"""
import os
import sys
from pathlib import Path

from cocotb_tools.runner import get_results, get_runner

SIMULATOR = "ghdl"
VHDL_VERSION = "08"


def _project_root(start):
    for parent in Path(start).resolve().parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    raise FileNotFoundError("Could not locate project root (pyproject.toml)")


def run_cocotb(*, sources, hdl_toplevel, test_module, caller_file, parameters=None):
    """Build and run a cocotb testbench with GHDL.

    Args:
        sources: RTL source paths, relative to the project root.
        hdl_toplevel: Name of the HDL toplevel entity.
        test_module: Name of the Python cocotb test module.
        caller_file: ``__file__`` of the calling ``test_run.py``.
        parameters: Optional generic/parameter overrides for the toplevel.
    """
    os.environ["SIM"] = os.getenv("SIM", SIMULATOR)
    os.environ["COCOTB_ANSI_OUTPUT"] = "1"

    # Make the test module importable regardless of how test_run.py is invoked.
    test_dir = Path(caller_file).resolve().parent
    if str(test_dir) not in sys.path:
        sys.path.insert(0, str(test_dir))

    root = _project_root(caller_file)
    abs_sources = [os.path.join(root, s) for s in sources]

    # Optionally restrict to a single cocotb testcase during development, e.g.
    # ``COCOTB_TESTCASE=debounce_test uv run pytest debounce/tb/debounce/test_run.py``.
    testcase = os.getenv("COCOTB_TESTCASE") or None

    build_args = ["--std={}".format(VHDL_VERSION), "-frelaxed-rules"]
    runner = get_runner(os.environ["SIM"])
    runner.build(
        sources=abs_sources,
        hdl_toplevel=hdl_toplevel,
        build_args=build_args,
        waves=True,
    )
    results_xml = runner.test(
        test_module=test_module,
        hdl_toplevel=hdl_toplevel,
        hdl_toplevel_lang="vhdl",
        testcase=testcase,
        parameters=parameters,
        test_args=build_args,
        plusargs=["--ieee-asserts=disable-at-0"],
        waves=True,
    )
    num_tests, num_failed = get_results(results_xml)
    assert num_failed == 0, "{} of {} tests failed".format(num_failed, num_tests)
