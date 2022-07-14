import math
from scripts.python.errors import CLK_ERROR, DEL_ERROR, check_code


def read_del(line):
    return line.split()[1], line.split()[2]

# def sort_dict(d):
#     d_sort = dict()
#     keys = sorted(d, key=d.get)

#     for k in keys:
#         d_sort[k] = d[k]

#     return d_sort

def create_conf_file_v():
    in_del = dict()
    gate_del = dict()
    simulations = 0
    clk = 0
    in_size = 0
    out_size = 0

    file = "./config/config.conf"

    with open(file) as conf:
        for line in conf:
            if line.startswith("sim"):
                simulations = int(line.split()[1])

            elif line.startswith("clk"):
                clk = int(line.split()[1])

            elif line.startswith("in_size"):
                in_size = int(line.split()[1])

            elif line.startswith("out_size"):
                out_size = int(line.split()[1])

            elif line.startswith("input"):
                data = read_del(line)
                in_del[data[0]] = data[1]

            elif line.startswith("gate"):
                data = read_del(line)
                gate_del[data[0]] = data[1]

    if simulations == 0:
        simulations = len(in_del)**2

    if clk == 0:
        check_code(CLK_ERROR)

    if in_size != len(in_del):
        check_code(DEL_ERROR)

    write_config_v(in_del, gate_del, simulations, clk, in_size, out_size)

def write_config_v(in_del, gate_del, sim, clk, in_size, out_size):
    with open("./config/config.v", "a") as conf:
        conf.truncate(0)

        # config file for number of simulations
        r = int(math.sqrt(sim))
        conf.write("`define SIM " + str(r) + "\n")
        conf.write("`define CLK_PERIOD #" + str(clk) + "\n")
        conf.write("`define IN_SIZE " + str(in_size) + "\n")
        conf.write("`define OUT_SIZE " + str(out_size) + "\n")

        conf.write("\n")

        # config file for gate delays
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

        #config file for input delays
        conf.write("`ifdef DEL\n")
        for i in in_del:
            string = "  `define " + i + " #" + in_del[i] + "\n"
            conf.write(string)
        conf.write("`else\n")
        for i in in_del:
            string = "  `define " + i + " #0\n"
            conf.write(string)
        conf.write("`endif\n")

def config():
    create_conf_file_v()