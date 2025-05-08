# Error Correction Code (ECC)
## About the IP
ECC encoder and decoder core with axi-stream like interface.

## Design Considerations
Number of parrity bits need to satisfy hamming theorem

2**C_NR_PARITY >= C_DATA_WIDTH + C_NR_PARITY + 2

For example:
* Max data bits with "C_NR_PARITY <= 6" equals to 56
* Max data bits with "C_NR_PARITY <= 7" equals to 119

## Prerequsits
* Cocotb to run testbench

## Test Bench
Setup cocotb to run the tb. For more information, please read the cocotb documentation.
https://www.cocotb.org/

### Run all
```
cb tb
make
```
### Run single module
```
cb tb/ecc_encode
make
```

