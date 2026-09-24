# Error Correction Code (ECC)

## About the IP

SEC-DED (single-error-correct, double-error-detect) Hamming encoder and decoder
with an AXI-stream-like `valid`/`ready` handshake. The encoder appends the Hamming
parity bits plus one overall parity bit; the decoder recomputes the syndrome,
corrects a single-bit error, and flags an uncorrectable (double-bit) error.

## Generics

Both `ecc_encode` and `ecc_decode` share the same generics:

| Generic        | Type        | Range / Default   | Description                          |
|----------------|-------------|-------------------|--------------------------------------|
| `C_ODD_PARITY` | `std_logic` | `'1'`             | Parity polarity (`'1'` = odd).       |
| `C_DATA_WIDTH` | `natural`   | `32..64`, def. 33 | Payload data width in bits.          |
| `C_NR_PARITY`  | `natural`   | `6..7`, def. 6    | Number of Hamming parity bits.       |

## Interface

Encoded word width is `C_DATA_WIDTH + C_NR_PARITY + 1`.

| Port        | Dir | Width                          | Notes                        |
|-------------|-----|--------------------------------|------------------------------|
| `clk`       | in  | 1                              | Clock.                       |
| `rst`       | in  | 1                              | Synchronous, active high.    |
| `in_data`   | in  | encoder: `C_DATA_WIDTH`        | decoder: encoded word width  |
| `in_valid`  | in  | 1                              | Input handshake.             |
| `in_ready`  | out | 1                              | Input handshake.             |
| `out_data`  | out | encoder: encoded word width    | decoder: `C_DATA_WIDTH`      |
| `out_valid` | out | 1                              | Output handshake.            |
| `out_ready` | in  | 1                              | Output handshake.            |
| `out_is_err`| out | 1                              | Decoder only: double error.  |

**Latency:** encoder = 2 clock cycles, decoder = 1 clock cycle.

## Design considerations

The number of parity bits must satisfy the Hamming inequality:

```
2**C_NR_PARITY >= C_DATA_WIDTH + C_NR_PARITY + 2
```

For example:
* Max data bits with `C_NR_PARITY = 6` is 56.
* Max data bits with `C_NR_PARITY = 7` is 119.

## Prerequisites

* [uv](https://docs.astral.sh/uv/) as the Python package manager.
* [GHDL](https://ghdl.github.io/ghdl/) as the simulator.

## Testbench

Testbenches use [cocotb](https://www.cocotb.org/) and check the HDL against an
independent Python reference model (`tb/utils/ecc.py`). Run from the repository root:

```
# All ECC testbenches
uv run pytest ecc/tb

# A single module
uv run pytest ecc/tb/ecc_encode/test_run.py
```
