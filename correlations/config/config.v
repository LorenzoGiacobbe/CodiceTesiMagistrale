`define SIM 16
`define CLK_PERIOD 5
`define IN_SIZE 4
`define OUT_SIZE 1

`ifdef DEL
  `define XNOR_DELAY #0.10
  `define NAND_DELAY #0.20
  `define XOR_DELAY #0.50
`else
  `define XNOR_DELAY #0
  `define NAND_DELAY #0
  `define XOR_DELAY #0
`endif

`ifdef IN_DEL
  `define a #0.02
  `define b #0.45
  `define r1 #0.00
  `define r2 #0.00
`else
  `define a #0
  `define b #0
  `define r1 #0
  `define r2 #0
`endif
