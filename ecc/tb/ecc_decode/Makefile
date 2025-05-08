TOPLEVEL_LANG ?= vhdl

SRC_PATH = $(shell pwd)/../../hdl
TB_PATH = $(shell pwd)/

VHDL_SOURCES = $(SRC_PATH)/rth_parity.vhd
VHDL_SOURCES += $(SRC_PATH)/ecc_decode.vhd
VHDL_SOURCES += $(SRC_PATH)/ecc_encode.vhd

TOPLEVEL := ecc_decode
MODULE := test_ecc
SIM=ghdl
VHDL_VERSION=08
EXTRA_ARGS= --std=$(VHDL_VERSION) -frelaxed-rules
SIM_ARGS= --wave=sim_build/wave.ghw --ieee-asserts=disable-at-0

include $(shell cocotb-config --makefiles)/Makefile.sim

.PHONY: gui sim clean_all
master: sim

gui: sim
	gtkwave sim_build/wave.out

clean_all: clean
	@rm -rf __pycache__
	@rm results.xml
