import subprocess
from scripts.python.create_interface import create_if

# gadget simulation
def simulate(module_name):
	tb = "./scripts/verilog/tb/tb.v"

	create_if(module_name)

	log = "./logs/vvp_log.log"
	log_del = "./logs/vvp_log_del.log"
	log_in_del = "./logs/vvp_log_in_del.log"

	subprocess.call(["./scripts/bash/sim.sh", "-t", tb])
	subprocess.call(["./scripts/bash/sim.sh", "-d", "-t", tb])
	subprocess.call(["./scripts/bash/sim.sh", "-D", "-t", tb])

	return log, log_del, log_in_del
