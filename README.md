[![MIT License](https://img.shields.io/github/license/casptri/hdl-core)](LICENSE.txt)

# hdl-core

A growing collection of reusable VHDL IP cores, each with a [cocotb](https://www.cocotb.org/) testbench and a Python reference model for verification.

## Cores

| Core | Description |
|------|-------------|
| [`ecc`](ecc/) | SECDED Hamming encoder and decoder with AXI-stream interface. Configurable data width (32–64 bit) and parity bits. |
| [`skid_buffer`](skid_buffer/) | AXI-stream skid buffer. Decouples upstream and downstream handshake logic with one cycle of pipeline latency. |
| [`debounce`](debounce/) | Multi-signal debounce filter. Configurable debounce time and number of signals. |

Each core has its own README with design notes and testbench instructions.

## Testing

Testbenches are written in Python using [cocotb](https://www.cocotb.org/) with [GHDL](https://ghdl.github.io/ghdl/) as the simulator. Each core includes a software reference model that independently computes the expected output, which is compared against the HDL simulation result.

## Roadmap

- [ ] Moving average filter
- [ ] I2C master
- [ ] SPI master
- [ ] AXI-Lite slave
- [ ] AXI-Lite master
- [ ] PID controller

## License

MIT — see [LICENSE.txt](LICENSE.txt)
