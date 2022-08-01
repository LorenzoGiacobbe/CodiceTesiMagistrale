`include "./scripts/verilog/src/dom.v"
`include "./config/config.v"

`timescale 1ns/1fs

module interface(VGND, VPWR, clk, in, out);

	input VGND, VPWR, clk;
	input [`IN_SIZE-1:0] in;

	output [`OUT_SIZE-1:0] out;

	wire [`IN_SIZE-1:0] in_del;

	assign `a0 in_del[13] = in[13];
	assign `a1 in_del[12] = in[12];
	assign `a2 in_del[11] = in[11];
	assign `a3 in_del[10] = in[10];
	assign `b0 in_del[9] = in[9];
	assign `b1 in_del[8] = in[8];
	assign `b2 in_del[7] = in[7];
	assign `b3 in_del[6] = in[6];
	assign `rand0 in_del[5] = in[5];
	assign `rand1 in_del[4] = in[4];
	assign `rand2 in_del[3] = in[3];
	assign `rand3 in_del[2] = in[2];
	assign `rand4 in_del[1] = in[1];
	assign `rand5 in_del[0] = in[0];

	`ifdef CLK
		dom test(.VGND(VGND), .VPWR(VPWR), .clk(clk), .in(in), .out(out));
	`else
		dom test(.VGND(VGND), .VPWR(VPWR), .in(in), .out(out));
	`endif

endmodule
