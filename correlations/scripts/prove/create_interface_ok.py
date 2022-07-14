def read_del_name(line):
    return line.split()[1]

def create_if(module_name):
    fn = "./scripts/verilog/interface/interface.v"
    with open(fn, "w") as interface:
        interface.write('`include "./' + module_name + '.v"\n')
        interface.write('`include "./config.v"\n\n')
        interface.write('`timescale 1ns/1fs\n\n')
        interface.write('module interface(VGND, VPWR, clk, in, out);\n\n')
        interface.write('\tinput VGND, VPWR, clk;\n')
        interface.write('\tinput [`IN_SIZE-1:0] in;\n\n')
        interface.write('\toutput [`OUT_SIZE-1:0] out;\n\n')
        interface.write('\twire [`IN_SIZE-1:0] in_del;\n\n')

        # loop to insert delays in inputs
        with open("./config.conf", "r") as conf:
            d = 0
            for line in conf:
                if line.startswith("input"):
                    interface.write('\tassign `' + read_del_name(line) + ' in_del[' + str(d) + '] = in[' + str(d) + '];\n')
                    d += 1

        interface.write('\n\t`ifdef clk\n')
        interface.write('\t\t' + module_name + ' test(.VGND(VGND), .VPWR(VPWR), .clk(clk), .in(in), .y(out));\n')
        interface.write('\t`else\n')
        interface.write('\t\t' + module_name + ' test(.VGND(VGND), .VPWR(VPWR), .in(in), .y(out));\n')
        interface.write('\t`endif\n\n')
        
        
        interface.write('endmodule\n')