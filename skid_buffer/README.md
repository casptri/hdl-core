# Skid buffer

## About the IP

Skid buffer with an AXI-stream interface. A skid buffer decouples an upstream and
downstream AXI-stream by registering both the data and the flow-control bits,
adding one cycle of pipeline latency while maintaining full throughput.

## Generics

| Generic      | Type      | Default | Description              |
|--------------|-----------|---------|--------------------------|
| `data_width` | `integer` | 8       | AXI-stream `tdata` width |

## Interface

Standard AXI-stream slave (`s_*`) and master (`m_*`) channels plus `clk` / `rst`
(synchronous, active high): `tdata`, `tvalid`, `tready`.

## Prerequisites

* [uv](https://docs.astral.sh/uv/) as the Python package manager.
* [GHDL](https://ghdl.github.io/ghdl/) as the simulator.

## Testbench

Testbenches use [cocotb](https://www.cocotb.org/) with
[cocotbext-axi](https://github.com/alexforencich/cocotbext-axi). Run from the
repository root:

```
uv run pytest skid_buffer/tb
```
