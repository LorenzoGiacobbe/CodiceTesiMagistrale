import math

def read_del(line):
    return line.split()[1], line.split()[2]

def sort_dict(d):
    d_sort = dict()
    keys = sorted(d, key=d.get)

    for k in keys:
        d_sort[k] = d[k]

    return d_sort

def read_conf_file(file):
    in_del = dict()
    gate_del = dict()
    simulations = 0

    with open(file) as conf:
        for line in conf:
            if line.startswith("input"):
                data = read_del(line)
                in_del[data[0]] = data[1]

            elif line.startswith("gate"):
                data = read_del(line)
                gate_del[data[0]] = data[1]

            elif line.startswith("sim"):
                simulations = int(line.split()[1])



    if simulations == 0:
        simulations = len(in_del)**2

    return sort_dict(in_del), sort_dict(gate_del), simulations

def write_config_v(file, in_del, gate_del, sim):
    with open("./config/config.v", "a") as conf:
        conf.truncate(0)

        # config file for number of simulations
        r = int(math.sqrt(sim))
        conf.write("`define SIM " + str(r) + "\n")

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

def config(file):
    data = read_conf_file(file)
    write_config_v(file, data[0], data[1], data[2])