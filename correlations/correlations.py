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
    bit_diff = list()

    for i in range(0, len):
        s = format(i, '04b')
        il.append(s)

    for i in range(len):
        for j in range(len):
            pre.append(i) #il[i])
            post.append(j) #il[j])
            bit_diff.append(diff(il[i], il[j]))
            
    return pre, post, bit_diff

def create_corr_table(log):

    toggles = create_toggle_list(log)
    t_len = math.sqrt(len(toggles))
    inputs = create_input_list(int(t_len))

    data = {"starting input": inputs[0], "new input": inputs[1], "diff bits": inputs[2], "number of toggles": toggles}

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

def pearsons_correlation_diff(df):
    
    diff = df.iloc[:, 2].to_frame()
    toggles = df.iloc[:, 3].to_frame()
    
    df = pd.concat([diff, toggles], axis=1)
    
    # columns = ['inputs', 'toggles']
    # df.columns = columns
    
    corr_table = df.corr(method='pearson')
    print(corr_table)
    print("------------------------------------------------------------")
    
    return corr_table
    
def pearsons_correlation_in(df):
    
    inputs = df.iloc[:, 1].to_frame()
    toggles = df.iloc[:, 3].to_frame()
    
    df = pd.concat([inputs, toggles], axis=1)
    
    # columns = ['inputs', 'toggles']
    # df.columns = columns
    
    corr_table = df.corr(method='pearson')
    print(corr_table)
    print("------------------------------------------------------------")
    
    return corr_table

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
    
    print()
    print("Correlation with inputs:")
    corr_table = pearsons_correlation_in(df)
    corr_table_del = pearsons_correlation_in(df_del)
    corr_table_in_del = pearsons_correlation_in(df_in_del)

    print()
    print("Correlation with bit changes:")
    corr_table = pearsons_correlation_diff(df)
    corr_table_del = pearsons_correlation_diff(df_del)
    corr_table_in_del = pearsons_correlation_diff(df_in_del)

    with pd.ExcelWriter("./spreadsheets/" + spreadsheet + ".xlsx") as writer:
        df.to_excel(writer, index=False, sheet_name="without delays")
        df_del.to_excel(writer, index=False, sheet_name="gate delays")
        df_in_del.to_excel(writer, index=False, sheet_name="gate+input delays")
        corr_table.to_excel(writer, sheet_name="corr table")
        corr_table_del.to_excel(writer, sheet_name="corr table gate delays")
        corr_table_in_del.to_excel(writer, sheet_name="corr table gate+input delays")
        
    print("spreadsheet with results saved in " + os.getcwd() + "/spreadsheets/" + spreadsheet + ".xlsx")

