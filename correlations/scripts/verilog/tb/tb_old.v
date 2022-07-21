`include "./scripts/verilog/interface/interface.v"
`include "./config/config.v"

`timescale 1ns/1fs

module tb;

reg [`IN_SIZE-1:0] in;
reg VPWR, VGND, clk;

initial clk = 0;
always `CLK_PERIOD clk = ~clk;

wire [`OUT_SIZE-1:0] out;

interface uut(
	.VPWR(VPWR), .VGND(VGND), .clk(clk),
    .in(in), .out(out)
	);

integer i;
integer j;
integer sim;

// simulation	
initial begin

	$dumpfile("./scripts/verilog/vcd/correlation.vcd");
	$dumpvars(0, tb);

	VPWR = 1'b1;
	VGND = 1'b0;
	sim = 0;

	$monitor("out: %b", out);

	`ifdef FULL
		for (i = 0; i < `SIM; i++) begin
			for (j = 0; j < `SIM; j++) begin
				in = i; `CLK_PERIOD;
				$display("BEGIN SIM %d", sim);
				sim++;
				in = j; `CLK_PERIOD;
				$display("END");
			end
		end
	`else
		for (i = 0; i < `SIM; i++) begin
			for (j = 0; j < `SIM; j++) begin
				in = {$random} % 2**`IN_SIZE; `CLK_PERIOD;
				$display("BEGIN SIM %d", sim);
				sim++;
				in = {$random} % 2**`IN_SIZE; `CLK_PERIOD;
				$display("END");
			end
		end
	`endif

	$finish;
end

endmodule  