`include "./scripts/verilog/src/2_gates_old.v"

`include "./config/config.v"

`timescale 1ns/1fs

module correlation_2_tb;
reg a, b, r1, r2;
reg VPWR, VGND;

wire y1, y2;

module_2_gates uut_r(
	.VPWR(VPWR), .VGND(VGND),
	.a(a), .b(b), .r1(r1), .r2(r2), .y(y1)
	);

integer i;
integer j;
integer sim;

// simulation	
initial begin

	$dumpfile("./scripts/verilog/vcd/correlation_old.vcd");
	$dumpvars(0, correlation_2_tb);

	VPWR = 1'b1;
	VGND = 1'b0;
	sim = 0;

	$monitor("out: %b", y1);

	for (i = 0; i < `SIM; i++) begin
		for (j = 0; j < `SIM; j++) begin
			{a, b, r1, r2} = i; #5;
			$display("BEGIN SIM %d", sim);
			sim++;
			{a, b, r1, r2} = j; #5;
			$display("END");
		end
	end 

	$finish;
end

endmodule  
