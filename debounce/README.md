# Debounce

## About the IP

Debounce filter for `N` parallel signals. Each input is synchronized through two
flip-flops and then gated by a per-signal down-counter: the counter reloads on
every input transition, and the output only follows the input once it has been
stable for `debounce_time` clock cycles.

## Generics

| Generic         | Type      | Default | Description                                  |
|-----------------|-----------|---------|----------------------------------------------|
| `nr_of_signal`  | `integer` | 1       | Number of independent signals to debounce.   |
| `debounce_time` | `integer` | 100     | Required stable time, in clock cycles.       |

## Interface

| Port      | Dir | Width            | Description                  |
|-----------|-----|------------------|------------------------------|
| `clk`     | in  | 1                | Clock.                       |
| `rst`     | in  | 1                | Synchronous, active high.    |
| `sig_in`  | in  | `nr_of_signal`   | Raw (bouncy) inputs.         |
| `sig_out` | out | `nr_of_signal`   | Debounced outputs.           |

## Prerequisites

* [uv](https://docs.astral.sh/uv/) as the Python package manager.
* [GHDL](https://ghdl.github.io/ghdl/) as the simulator.

## Testbench

Run from the repository root:

```
uv run pytest debounce/tb
```
