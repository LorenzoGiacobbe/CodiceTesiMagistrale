`include "./scripts/verilog/src/module_2_gates.v"
`include "./config/config.v"

`timescale 1ns/1fs

module interface(VGND, VPWR, clk, in, out);

	input VGND, VPWR, clk;
	input [`IN_SIZE-1:0] in;

	output [`OUT_SIZE-1:0] out;

	wire [`IN_SIZE-1:0] in_del;

	assign `a in_del[3] = in[3];
	assign `b in_del[2] = in[2];
	assign `r1 in_del[1] = in[1];
	assign `r2 in_del[0] = in[0];

	`ifdef CLK
		module_2_gates test(.VGND(VGND), .VPWR(VPWR), .clk(clk), .in(in), .out(out));
	`else
		module_2_gates test(.VGND(VGND), .VPWR(VPWR), .in(in), .out(out));
	`endif

endmodule
