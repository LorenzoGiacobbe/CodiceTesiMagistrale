import subprocess
from scripts.python.create_interface import create_if

# gadget simulation
def simulate(module_name, conf_file):
	tb = "./scripts/verilog/tb/tb.v"

	# function automatically generating the general interface for the gadget
	create_if(module_name, conf_file)

	# location of the log files containing the results of the simulations:
	# 	- log: 			simulation without delays
	#	- log_del:		simulation with gate delays
	#	- log_in_del:	simulation with gate and input delays	
	log = "./logs/vvp_log.log"
	log_del = "./logs/vvp_log_del.log"
	log_in_del = "./logs/vvp_log_in_del.log"

	# the sim.sh script is called wich uses iverilog to compile and vvp
	# to simulate the testbench passed as argument
	subprocess.call(["./scripts/bash/sim.sh", "-t", tb])
	subprocess.call(["./scripts/bash/sim.sh", "-d", "-t", tb])
	subprocess.call(["./scripts/bash/sim.sh", "-D", "-t", tb])

	return log, log_del, log_in_del
