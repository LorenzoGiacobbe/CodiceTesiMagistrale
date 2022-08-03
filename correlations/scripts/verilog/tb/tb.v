`include "./scripts/verilog/interface/interface.v"
`include "./config/config.v"

`timescale 1ns/1fs
`define NULL 0

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
reg [`IN_SIZE-1:0] pre_data;
reg [`IN_SIZE-1:0] post_data;

// da vedere se posso cancellarlo
integer scan_file;
integer check;

// simulation	
initial begin

	$dumpfile("./scripts/verilog/vcd/correlation.vcd");
	$dumpvars(0, tb);

	VPWR = 1'b1;
	VGND = 1'b0;
	sim = 0;

    // check = $fopen("./scripts/prove/check.dat", "w");
    // if (check == `NULL) begin
    //     $display("check.dat handle was NULL");
    //     $finish;
    // end

    inputs = $fopen("./config/inputs.dat", "r");
    if (inputs == `NULL) begin
        $display("inputs.dat handle was NULL");
        $finish;
    end 
    else begin
        $monitor("out: %b", out);
        for (i = 0; i < `SIM; i++) begin
			for (j = 0; j < `SIM; j++) begin
                scan_file = $fscanf(inputs, "%d\n%d\n", pre_data, post_data); 
                if (!$feof(inputs)) begin
                    // here i have read the inputs input
                    in = pre_data;
                    #(`CLK_PERIOD);
                    $write("BEGIN SIM %d\n", sim);
                    sim++;
                    in = post_data;
                    #(`CLK_PERIOD);
                    $write("END\n");
                end
            end
        end
    end

	$fclose(inputs);

	$finish;
end

endmodule  