import pandas as pd
import numpy as np
import subprocess
import sys
import os
import math

def diff(s1, s2):
	count = 0
	for i in range(len(s1)):
		if s1[i] != s2[i]:
			count = count +1
	return count

# User interaction
def get_inputs():
	tb = input("insert the path of testbench to execute:")
	spreadsheet = input("insert the name of the spreadsheet:")
	
	return tb, spreadsheet

# Error handling
def check_code(code):
	if code != 1:
		sim_error()
		sys.exit()

def sim_error():
    	print("Something went wrong with the execution")

# Toggle lists creation
def create_toggle_list(vvp_log):
	tl = list()

	with open(vvp_log) as log:
		toggles = 0
		sim = 0
		for line in log:
			if line.startswith("BEGIN"):
				toggles = 0
				sim = sim + 1
			elif line.startswith("END"):
				tl.append(toggles)
			elif line.startswith("out"):
				toggles = toggles + 1

	return tl

def create_input_list(len):
	il = list()
	pre = list()
	post = list()
	ab = list()
	bit_diff = list()
	passaggio = list()

	for i in range(0, len):
		s = format(i, '04b')
		il.append(s)

	for i in range(len):
		for j in range(len):
			pre.append(il[i])
			post.append(il[j])
			ab.append(((i//4)*16)+(j//4))
			bit_diff.append(diff(il[i], il[j]))
			passaggio.append((i*16)+j)
	    
	return pre, post, ab, passaggio, bit_diff

def create_corr_table(log):

	toggles = create_toggle_list(log)
	t_len = math.sqrt(len(toggles))
	inputs = create_input_list(int(t_len))

	data = {"starting input": inputs[0], "new input": inputs[1], "passaggio ab": inputs[2], "passaggio ID": inputs[3], "diff bits": inputs[4], "number of toggles": toggles}

	df = pd.DataFrame(data = data)

	return df

def simulate(tb):
	log = "./logs/vvp_log"
	log_del = "./logs/vvp_log_del"
	log_in_del = "./logs/vvp_log_in_del"

	exit_code = subprocess.call(["./scripts/sim.sh", "-t", tb])
	check_code(exit_code)
	exit_code = subprocess.call(["./scripts/sim.sh", "-d", "-t", tb])
	check_code(exit_code)
	exit_code = subprocess.call(["./scripts/sim.sh", "-D", "-t", tb])
	check_code(exit_code)

	return log, log_del, log_in_del

def pearsons_correlation(df, df_del, df_in_del, col1, col2):
    	# calculate correlation for df without delays
	inputs = df.iloc[:, col1].to_frame()
	toggles = df.iloc[:, col2].to_frame()

	df = pd.concat([inputs, toggles], axis=1)

	corr_table = df.corr(method='pearson')
	
	# calculate correlation for df with gate delays
	inputs = df_del.iloc[:, col1].to_frame()
	toggles = df_del.iloc[:, col2].to_frame()

	df = pd.concat([inputs, toggles], axis=1)

	corr_table_del = df.corr(method='pearson')
	
	# calculate correlation for df with gate and input delays
	inputs = df_in_del.iloc[:, col1].to_frame()
	toggles = df_in_del.iloc[:, col2].to_frame()

	df = pd.concat([inputs, toggles], axis=1)

	corr_table_in_del = df.corr(method='pearson')

	return corr_table, corr_table_del, corr_table_in_del

if __name__ == "__main__": 

	tb = "./verilog/tb/correlation_tb.v"
	spreadsheet = sys.argv[1]

	#ui = get_inputs() # 0 = tesbench; 1 = spreadsheet
	#tb = ui[0]
	#spreadsheet = ui[1]

	vvp_logs = simulate(tb)

	df = create_corr_table(vvp_logs[0])
	df_del = create_corr_table(vvp_logs[1])
	df_in_del = create_corr_table(vvp_logs[2])

	with pd.ExcelWriter("./spreadsheets/" + spreadsheet + ".xlsx") as writer:
		# write starting tables on excel workbook
		df.to_excel(writer, index=False, sheet_name="Without delays")
		df_del.to_excel(writer, index=False, sheet_name="Gate delays")
		df_in_del.to_excel(writer, index=False, sheet_name="Gate+input delays")
		
		# write correlation table for transition from old to new state of all inputs
		corr_tables = pearsons_correlation(df, df_del, df_in_del, 3, 5)
		corr_tables[0].to_excel(writer, sheet_name="Corr tables", startrow=0, startcol=0)
		corr_tables[1].to_excel(writer, sheet_name="Corr tables", startrow=0, startcol=5)
		corr_tables[2].to_excel(writer, sheet_name="Corr tables", startrow=0, startcol=10)
		
		# write correlation table for transition from old to new state of a and b
		corr_tables = pearsons_correlation(df, df_del, df_in_del, 2, 5)
		corr_tables[0].to_excel(writer, sheet_name="Corr tables", startrow=5, startcol=0)
		corr_tables[1].to_excel(writer, sheet_name="Corr tables", startrow=5, startcol=5)
		corr_tables[2].to_excel(writer, sheet_name="Corr tables", startrow=5, startcol=10)
		
		# write correlation table for the number of bits that change from old to new state
		corr_tables = pearsons_correlation(df, df_del, df_in_del, 4, 5)
		corr_tables[0].to_excel(writer, sheet_name="Corr tables", startrow=10, startcol=0)
		corr_tables[1].to_excel(writer, sheet_name="Corr tables", startrow=10, startcol=5)
		corr_tables[2].to_excel(writer, sheet_name="Corr tables", startrow=10, startcol=10)

	print("spreadsheet with results saved in " + os.getcwd() + "/spreadsheets/" + spreadsheet + ".xlsx")

