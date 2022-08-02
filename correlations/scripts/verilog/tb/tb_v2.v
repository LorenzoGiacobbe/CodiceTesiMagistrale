`include "./scripts/verilog/interface/interface.v"
`include "./config/config.v"

`timescale 1ns/1fs

module tb;

reg [`IN_SIZE-1:0] in;
reg VPWR, VGND, clk;

initial clk = 0;
always #(`CLK_PERIOD / 2) clk = ~clk;

wire [`OUT_SIZE-1:0] out;

interface uut(
	.VPWR(VPWR), .VGND(VGND), .clk(clk),
    .in(in), .out(out)
	);

integer i;
integer j;
integer sim;
integer inputs;

// simulation	
initial begin

	$dumpfile("./scripts/verilog/vcd/correlation.vcd");
	$dumpvars(0, tb);
	
	inputs = $fopen("./logs/inputs.txt", "w");
	//if(inputs) $display("inputs opened");

	VPWR = 1'b1;
	VGND = 1'b0;
	sim = 0;

	$monitor("out: %b", out);

	`ifdef FULL
		for (i = 0; i < `SIM; i++) begin
			for (j = 0; j < `SIM; j++) begin
				$fwrite(inputs, "%d\t%d\n", i, j);
				in = i; #(`CLK_PERIOD);
				$write("BEGIN SIM %d\n", sim);
				sim++;
				in = j; #(`CLK_PERIOD);
				$write("END\n");
			end
		end
	`else
		for (i = 0; i < `SIM; i++) begin
			for (j = 0; j < `SIM; j++) begin
				in = {$random} % 2**`IN_SIZE;
				$fwrite(inputs, "%d\t", in);
				#(`CLK_PERIOD);
				$write("BEGIN SIM %d\n", sim);
				sim++;
				in = {$random} % 2**`IN_SIZE;
				$fwrite(inputs, "%d\n", in);
				#(`CLK_PERIOD);
				$write("END\n");
			end
		end
	`endif

	$fclose(inputs);

	$finish;
end

endmodule  