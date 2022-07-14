import sys

# clock period not defined in the config file
CLK_ERROR = 1
# delay value missing for some input
DEL_ERROR = 2


# Error handling
def check_code(code):
	if code == CLK_ERROR:
		clk_error()
		sys.exit()
	if code == DEL_ERROR:
		del_error()
		sys.exit()

def clk_error():
    print("clock period not defined in the config file.")

def del_error():
	print("delay value missing for some inputs.")
