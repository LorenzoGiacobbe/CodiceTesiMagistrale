import math

from scripts.python.errors import CLK_ERROR, DEL_ERROR, check_code
from config.generate_inputs import gen_in
import config.global_vars as gv

# auxiliary function reading to help reading the configuration file
def read_del(line):
    return line.split()[1], line.split()[2]

def create_conf_file_v(file):
    in_del = dict()
    gate_del = dict()
    out_size = 0
    clk = 'y'
    period = 0

    # reads the configuration file and initializes all needed values
    with open(file) as conf:
        for line in conf:
            if line.startswith("sim"):
                gv.new_simulations(int(line.split()[1]))
            
            elif line.startswith("full"):
                f = line.split()[1]
                if f == 'n':
                    gv.new_full('n')

            elif line.startswith("clk"):
                clk = line.split()[1]

            elif line.startswith("period"):
                period = int(line.split()[1])

            elif line.startswith("in_size"):
                gv.new_in_size(int(line.split()[1]))

            elif line.startswith("rand_size"):
                gv.new_rand_size(int(line.split()[1]))

            elif line.startswith("out_size"):
                out_size = int(line.split()[1])

            elif line.startswith("input"):
                data = read_del(line)
                in_del[data[0]] = data[1]

            elif line.startswith("gate"):
                data = read_del(line)
                gate_del[data[0]] = data[1]

    if gv.simulations == 0:
        gv.new_simulations(len(in_del)**2)

    if clk == 0:
        check_code(CLK_ERROR)

    if (gv.in_size + gv.rand_size) != len(in_del):
        check_code(DEL_ERROR)

    # uses the values read before to write the verilog configuration file
    # containing all the definitions needed for the simulations
    write_config_v(in_del, gate_del, gv.simulations, clk, period, gv.in_size, gv.rand_size, out_size)

def write_config_v(in_del, gate_del, sim, clk, period, in_size, rand_size, out_size):
    file = "./config/config.v"
    with open(file, "a") as conf:
        conf.truncate(0)

        # write needed defines on the config.v file
        r = int(math.sqrt(sim))
        conf.write("`define SIM " + str(r) + "\n")
        if clk == 'y':
            conf.write("`define CLK\n")
        conf.write("`define CLK_PERIOD " + str(period) + "\n")
        conf.write("`define IN_SIZE " + str(in_size+rand_size) + "\n")
        conf.write("`define OUT_SIZE " + str(out_size) + "\n")

        conf.write("\n")

        # section of the config.v file containing the gate delays
        conf.write("`ifdef DEL\n")
        for i in gate_del:
            string = "  `define " + i + " #" + gate_del[i] + "\n"
            conf.write(string)
        conf.write("`else\n")
        for i in gate_del:
            string = "  `define " + i + " #0\n"
            conf.write(string)
        conf.write("`endif\n")

        conf.write("\n")

        # section of the config.v file containing the input delays
        conf.write("`ifdef IN_DEL\n")
        for i in in_del:
            string = "  `define " + i + " #" + in_del[i] + "\n"
            conf.write(string)
        conf.write("`else\n")
        for i in in_del:
            string = "  `define " + i + " #0\n"
            conf.write(string)
        conf.write("`endif\n")

def config(conf_file):
    # the configuration file is read and the config.v file generated
    create_conf_file_v(conf_file)
    # based on the full parameter of the configuration file the inputs are generated
    gen_in()