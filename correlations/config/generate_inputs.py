import os
import config.global_vars as gv

# generates the random inputs that are then used for the simulation
def gen_in():
    with open("./config/inputs.dat", "a") as inputs:
        inputs.truncate(0)

        # generate one input per line -> 2*(gv.simulations)
        #       2* because it has to generate one line for pre and one for post
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


    return