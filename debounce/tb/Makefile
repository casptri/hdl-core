# Author: Caspar Trittibach <ctrittibach@gmail.com>
#
# Copyright (c) 2021 Caspar Trittibach

TOPLEVEL_LANG ?= vhdl
SRC_PATH = $(shell pwd)/../hdl
TB_PATH = $(shell pwd)/

VHDL_SOURCES = $(SRC_PATH)/debounce.vhd

TOPLEVEL := debounce
MODULE := test_debounce
SIM = ghdl
VHDL_VERSION = 08
EXTRA_ARGS = "--std=$(VHDL_VERSION)"
#SIM_ARGS = --vcd=sim_build/wave.out --ieee-asserts=disable
SIM_ARGS = --wave=sim_build/wave.ghw --ieee-asserts=disable

include $(shell cocotb-config --makefiles)/Makefile.sim

clean_all: clean
	@rm -rf __pycache__
	@rm results.xml
