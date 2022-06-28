`timescale 1ns/1fs

`ifdef IN_DEL
	`include "./verilog/3_gates/synth/3_gates_in_del.v"
`else
	`include "./verilog/3_gates/synth/3_gates.v"
`endif


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

	$dumpfile("./verilog/tb/vcd/correlation.vcd");
	$dumpvars(0, correlation_3_tb);

	VPWR = 1'b1;
	VGND = 1'b0;
	sim = 0;

	$monitor("out: %b", y1);

	for (k = 0; k < 2; k++) begin
		q = k;
		for (i = 0; i < 16; i++) begin
			for (j = 0; j < 16; j++) begin
				{a, b, r1, r2} = i; #5;
				$display("BEGIN SIM %d", sim);
				sim++;
				{a, b, r1, r2} = j; #5;
				$display("END");
			end
		end 
	end

	$finish;
end

endmodule  