`define SIM 11
`define CLK
`define CLK_PERIOD 5
`define IN_SIZE 14
`define OUT_SIZE 4

`ifdef DEL
  `define XNOR_DELAY #0.10
  `define NAND_DELAY #0.20
  `define XOR_DELAY #0.50
  `define AND_DELAY #0.30
`else
  `define XNOR_DELAY #0
  `define NAND_DELAY #0
  `define XOR_DELAY #0
  `define AND_DELAY #0
`endif

`ifdef IN_DEL
  `define a0 #0.02
  `define a1 #0.04
  `define a2 #0.03
  `define a3 #0.10
  `define b0 #0.45
  `define b1 #0.22
  `define b2 #0.36
  `define b3 #0.51
  `define rand0 #0.00
  `define rand1 #0.00
  `define rand2 #0.00
  `define rand3 #0.00
  `define rand4 #0.00
  `define rand5 #0.00
`else
  `define a0 #0
  `define a1 #0
  `define a2 #0
  `define a3 #0
  `define b0 #0
  `define b1 #0
  `define b2 #0
  `define b3 #0
  `define rand0 #0
  `define rand1 #0
  `define rand2 #0
  `define rand3 #0
  `define rand4 #0
  `define rand5 #0
`endif
