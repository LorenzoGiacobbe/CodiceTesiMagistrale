`include "./scripts/verilog/src/gadget_robust.v"
`include "./config/config.v"

`timescale 1ns/1fs

module interface(VGND, VPWR, clk, in, out);

	input VGND, VPWR, clk;
	input [`IN_SIZE-1:0] in;

	output [`OUT_SIZE-1:0] out;

	wire [`IN_SIZE-1:0] in_del;

	assign `a0 in_del[23] = in[23];
	assign `a1 in_del[22] = in[22];
	assign `a2 in_del[21] = in[21];
	assign `a3 in_del[20] = in[20];
	assign `b0 in_del[19] = in[19];
	assign `b1 in_del[18] = in[18];
	assign `b2 in_del[17] = in[17];
	assign `b3 in_del[16] = in[16];
	assign `rand0 in_del[15] = in[15];
	assign `rand1 in_del[14] = in[14];
	assign `rand2 in_del[13] = in[13];
	assign `rand3 in_del[12] = in[12];
	assign `rand4 in_del[11] = in[11];
	assign `rand5 in_del[10] = in[10];
	assign `rand6 in_del[9] = in[9];
	assign `rand7 in_del[8] = in[8];
	assign `rand8 in_del[7] = in[7];
	assign `rand9 in_del[6] = in[6];
	assign `rand10 in_del[5] = in[5];
	assign `rand11 in_del[4] = in[4];
	assign `rand12 in_del[3] = in[3];
	assign `rand13 in_del[2] = in[2];
	assign `rand14 in_del[1] = in[1];
	assign `rand15 in_del[0] = in[0];

	`ifdef CLK
		gadget_robust test(.VGND(VGND), .VPWR(VPWR), .clk(clk), .in(in), .out(out));
	`else
		gadget_robust test(.VGND(VGND), .VPWR(VPWR), .in(in), .out(out));
	`endif

endmodule
