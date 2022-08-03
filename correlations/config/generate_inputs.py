import os
import config.global_vars as gv

def gen_in():
    with open("./config/inputs.dat", "a") as inputs:
        # potential old inputs are truncated
        inputs.truncate(0)

        # the full parameter has two possible values
        #   - y: all the possible input combinations have to be simulated
        #   - n: a subset of all simulations is simulated -> the inputs are generated randomically
        if(gv.full == 'y'):
            sim = (gv.in_size + gv.rand_size)**2
            for i in range(0, sim):
                for j in range(0, sim):
                    inputs.write(str(i) + "\n" + str(j) + '\n')
                    
        else:
            bytes_to_gen = int((gv.in_size+gv.rand_size)/8 + 1)
            for i in range(0, 2*(gv.simulations)):
                rand = int.from_bytes(os.urandom(bytes_to_gen), "big")
                inputs.write(str(rand) + "\n")