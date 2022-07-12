import subprocess

from scripts.python.errors import check_code

# gadget simulation
def simulate(tb):
	log = "./logs/vvp_log"
	log_del = "./logs/vvp_log_del"
	log_in_del = "./logs/vvp_log_in_del"

	exit_code = subprocess.call(["./scripts/bash/sim.sh", "-t", tb])
	check_code(exit_code)
	exit_code = subprocess.call(["./scripts/bash/sim.sh", "-d", "-t", tb])
	check_code(exit_code)
	exit_code = subprocess.call(["./scripts/bash/sim.sh", "-D", "-t", tb])
	check_code(exit_code)

	return log, log_del, log_in_del
