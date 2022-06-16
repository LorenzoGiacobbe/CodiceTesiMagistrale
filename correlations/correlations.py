import pandas as pd
import numpy as np
import subprocess
import sys
import os
import math

def hamming_distance(i1, i2):
	x = i1 ^ i2
	hd = 0
	
	while(x > 0):
		hd += x & 1
		x >>= 1
	
	return hd

def xor_str(s1, s2):
	x = tuple(a^b for a,b in zip(bytes(s1, encoding='utf8'), bytes(s2, encoding='utf8')))

	return int.from_bytes(bytes(x), 'big')

def my_xor(i1, i2):
	return i1 ^ i2
	
def my_and(i1, i2):
	return i1 & i2

def diff(s1, s2):
	count = 0
	for i in range(len(s1)):
		if s1[i] != s2[i]:
			count = count + 1
	return count
	
def legends():
	legends = list()

	# legend for input tables
	fields = list()
	expl = list()
	
	fields.append("Old values")
	expl.append("old values of the inputs before the new inputs are passed (a b r0 r1). E.g. 0110 represents a=0, b=1, r0=1, r1=0")
	fields.append("New values")
	expl.append("old values of the inputs (a b r0 r1). E.g. 0110 represents a=0, b=1, r0=1, r1=0")
	fields.append("AB change ID")
	expl.append("Unique ID for each different change of the old values of a and b")
	fields.append("Input change ID")
	expl.append("Unique ID for each different change of the old values of all inputs")
	fields.append("Hamming distance")
	expl.append("Hamming distance between old and new values of the inputs")
	fields.append("Toggles")
	expl.append("Number of toggles the output performs transitioning from the old to the new values")
	
	df = pd.DataFrame(data = {"Field": fields, "Explanation": expl})
	legends.append(df)


	return legends

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
	x = list()
	
	#ab = list()
	#bit_diff = list()
	#passaggio = list()

	for i in range(0, len):
		s = format(i, '04b')
		il.append(s)

	for i in range(len):
		for j in range(len):
			pre_a = int(il[i][0])
			pre_b = int(il[i][1])
			post_a = int(il[j][0])
			post_b = int(il[j][1])
			#post_r1 = int(il[j][2])
			#post_r2 = int(il[j][3])
			
			pre.append(il[i])
			post.append(il[j])
			
			#x.append(my_xor(
			#		my_xor(post_r1, post_r2), 
			#		my_and(post_a, post_b))
			#)
			
			#x.append(my_xor(pre_a+pre_b, post_a+post_b))
			#x.append(my_xor((pre_a<<1)+pre_b, (post_a<<1)+post_b))
			#x.append(my_and((pre_a<<1)+pre_b, (post_a<<1)+post_b))
			
			#x.append(my_xor(my_and(pre_a, pre_b), my_and(post_a, post_b))) # --> più alto	
			x.append(post_a)
			
			#x.append(my_and(my_xor(pre_a, pre_b), my_xor(post_a, post_b)))
			#x.append((my_and(pre_a, pre_b)<<1) + my_and(post_a, post_b))
			#x.append(my_and(
			#		my_xor(my_and(pre_a, pre_b), my_and(post_a, post_b)),
			#		my_xor(my_and(pre_a, post_a), my_and(pre_b, post_b))
			#	)) 
			#x.append(my_xor(
			#		my_xor(my_and(pre_a, pre_b), my_and(post_a, post_b)),
			#		my_and(my_and(pre_a, post_a), my_and(pre_b, post_b))
			#	))
			#x.append(hamming_distance(my_and(pre_a, pre_b), my_and(post_a, post_b))) # -> stesso risultato del più alto
			#x.append(my_and(
			#		hamming_distance(my_and(pre_a, pre_b), my_and(post_a, post_b)),
			#		hamming_distance(my_and(pre_a, post_a), my_and(pre_b, post_b))
			#))
			
						
			#ab.append(((i//4)*16)+(j//4))
			#bit_diff.append(diff(il[i], il[j]))
			#passaggio.append((i*16)+j)
	    
	return pre, post, x #ab, passaggio, bit_diff

def create_corr_table(log):

	toggles = create_toggle_list(log)
	t_len = math.sqrt(len(toggles))
	inputs = create_input_list(int(t_len))

	#data = {"Old values": inputs[0], "New values": inputs[1], "AB change ID": inputs[2], "Input change ID": inputs[3], "Hamming distance": inputs[4], "Toggles": toggles}

	data = {"Old values": inputs[0], "New values": inputs[1], "Toggles": toggles, "Input XOR": inputs[2]}

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
	print(corr_table)
	print("-----------------------------------------------------")
	print()
	
	# calculate correlation for df with gate delays
	inputs = df_del.iloc[:, col1].to_frame()
	toggles = df_del.iloc[:, col2].to_frame()

	df = pd.concat([inputs, toggles], axis=1)

	corr_table_del = df.corr(method='pearson')
	print(corr_table_del)
	print("-----------------------------------------------------")
	print()
	
	# calculate correlation for df with gate and input delays
	inputs = df_in_del.iloc[:, col1].to_frame()
	toggles = df_in_del.iloc[:, col2].to_frame()

	df = pd.concat([inputs, toggles], axis=1)

	corr_table_in_del = df.corr(method='pearson')
	print(corr_table_in_del)
	print("-----------------------------------------------------")
	print()


	return corr_table, corr_table_del, corr_table_in_del

if __name__ == "__main__": 

	tb = "./verilog/tb/correlation_tb.v"
	spreadsheet = sys.argv[1]

	#ui = get_inputs() # 0 = tesbench; 1 = spreadsheet
	#tb = ui[0]
	#spreadsheet = ui[1]

	vvp_logs = simulate(tb)

	df = create_corr_table(vvp_logs[0])
	#print(df)
	df_del = create_corr_table(vvp_logs[1])
	df_in_del = create_corr_table(vvp_logs[2])

	with pd.ExcelWriter("./spreadsheets/" + spreadsheet + ".xlsx") as writer:
		# write starting tables on excel workbook
		df.to_excel(writer, index=False, sheet_name="Without delays")
		#legends()[0].to_excel(writer, index=False, sheet_name="Without delays", startrow=0, startcol=8)
		#df_del.to_excel(writer, index=False, sheet_name="Gate delays")
		#legends()[0].to_excel(writer, index=False, sheet_name="Without delays", startrow=0, startcol=8)
		#df_in_del.to_excel(writer, index=False, sheet_name="Gate+input delays")
		#legends()[0].to_excel(writer, index=False, sheet_name="Without delays", startrow=0, startcol=8)
		
		# write correlation table for transition from old to new state of all inputs
		corr_tables = pearsons_correlation(df, df_del, df_in_del, 2, 3)
		#corr_tables[0].to_excel(writer, sheet_name="Corr tables", startrow=0, startcol=0)
		#corr_tables[1].to_excel(writer, sheet_name="Corr tables", startrow=0, startcol=5)
		#corr_tables[2].to_excel(writer, sheet_name="Corr tables", startrow=0, startcol=10)
		
		# write correlation table for transition from old to new state of all inputs
		#corr_tables = pearsons_correlation(df, df_del, df_in_del, 3, 5)
		#corr_tables[0].to_excel(writer, sheet_name="Corr tables", startrow=0, startcol=0)
		#corr_tables[1].to_excel(writer, sheet_name="Corr tables", startrow=0, startcol=5)
		#corr_tables[2].to_excel(writer, sheet_name="Corr tables", startrow=0, startcol=10)
		
		# write correlation table for transition from old to new state of a and b
		#corr_tables = pearsons_correlation(df, df_del, df_in_del, 2, 5)
		#corr_tables[0].to_excel(writer, sheet_name="Corr tables", startrow=5, startcol=0)
		#corr_tables[1].to_excel(writer, sheet_name="Corr tables", startrow=5, startcol=5)
		#corr_tables[2].to_excel(writer, sheet_name="Corr tables", startrow=5, startcol=10)
		
		# write correlation table for the number of bits that change from old to new state
		#corr_tables = pearsons_correlation(df, df_del, df_in_del, 4, 5)
		#corr_tables[0].to_excel(writer, sheet_name="Corr tables", startrow=10, startcol=0)
		#corr_tables[1].to_excel(writer, sheet_name="Corr tables", startrow=10, startcol=5)
		#corr_tables[2].to_excel(writer, sheet_name="Corr tables", startrow=10, startcol=10)

	#print("spreadsheet with results saved in " + os.getcwd() + "/spreadsheets/" + spreadsheet + ".xlsx")

