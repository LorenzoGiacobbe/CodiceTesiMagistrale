`define SIM 16

`ifdef DEL
  `define XNOR_DELAY #0.10
  `define NAND_DELAY #0.20
  `define XOR_DELAY #0.50
`else
  `define XNOR_DELAY #0
  `define NAND_DELAY #0
  `define XOR_DELAY #0
`endif

`ifdef DEL
  `define r1 #0.00
  `define r2 #0.00
  `define a #0.02
  `define b #0.45
`else
  `define r1 #0
  `define r2 #0
  `define a #0
  `define b #0
`endif
