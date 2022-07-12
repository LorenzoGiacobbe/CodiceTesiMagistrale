`include "./scripts/verilog/src/3_gates.v"

`include "./config/config.v"

`timescale 1ns/1fs

module correlation_3_tb;
reg a, b, r1, r2, q;
reg VPWR, VGND;

wire y1;

module_3_gates uut_r(
	.VPWR(VPWR), .VGND(VGND),
	.a(a), .b(b), .r1(r1), .r2(r2), .q(q), .y(y1)
	);

integer i;
integer j;
integer k;
integer sim;

// simulation	
initial begin

	$dumpfile("./scripts/verilog/vcd/correlation.vcd");
	$dumpvars(0, correlation_3_tb);

	VPWR = 1'b1;
	VGND = 1'b0;
	sim = 0;

	$monitor("out: %b", y1);

	for (i = 0; i < 32; i++) begin
		for (j = 0; j < 32; j++) begin
			{a, b, r1, r2, q} = i; #5;
			$display("BEGIN SIM %d", sim);
			sim++;
			{a, b, r1, r2, q} = j; #5;
			$display("END");
		end
	end

	$finish;
end

endmodule  