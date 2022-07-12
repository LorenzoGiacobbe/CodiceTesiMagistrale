`timescale 1ns/1fs

`ifdef IN_DEL
	`include "./verilog/2_gates/synth/2_gates_in_del.v"
`else
	`include "./verilog/2_gates/synth/2_gates.v"
`endif


module correlation_2_tb;
reg a, b, r1, r2;
reg VPWR, VGND;

wire y1;

module_2_gates uut_r(
	.VPWR(VPWR), .VGND(VGND),
	.a(a), .b(b), .r1(r1), .r2(r2), .y(y1)
	);

integer i;
integer j;
integer sim;

// simulation	
initial begin

	$dumpfile("./verilog/tb/vcd/correlation.vcd");
	$dumpvars(0, correlation_2_tb);

	VPWR = 1'b1;
	VGND = 1'b0;
	sim = 0;

	$monitor("out: %b", y1);

	for (i = 0; i < 16; i++) begin
		for (j = 0; j < 16; j++) begin
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