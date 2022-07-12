import sys

# Error handling
def check_code(code):
	if code != 1:
		sim_error()
		sys.exit()

def sim_error():
    	print("Something went wrong with the execution")
