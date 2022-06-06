import pandas as pd
import numpy as np
import subprocess
import sys
import os
import math

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

    for i in range(0, len):
        s = str(format(i, '04b'))
        il.append(s)

    for i in range(0, len):
        for j in range(0, len):
            pre.append(il[i])
            post.append(il[j])

    return pre, post

def create_corr_table(log):

    toggles = create_toggle_list(log)
    t_len = math.sqrt(len(toggles))
    inputs = create_input_list(int(t_len))

    data = {"starting input": inputs[0], "new input": inputs[1], "number of toggles": toggles}

    df = pd.DataFrame(data = data)
    
    return df
    
def new_create_corr_table(log):

    toggles = create_toggle_list(log)
    t_len = math.sqrt(len(toggles))
    inputs = create_input_list(int(t_len))

    data = {"number of toggles": toggles}

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

def pearsons_correlation(df1, df2):

    df1 = df1.iloc[:, 2].to_frame()
    df2 = df2.iloc[:, 2].to_frame()
    
    df = pd.concat([df1, df2], axis=1)
    
    # columns = ['col1', 'col2']
    # df.columns = columns
    
    corr_table = df.corr(method='pearson')
    
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

    corr_table = pearsons_correlation(df, df)

    with pd.ExcelWriter("./spreadsheets/" + spreadsheet + ".xlsx") as writer:
        df.to_excel(writer, index=False, sheet_name="without delays")
        df_del.to_excel(writer, index=False, sheet_name="gate delays")
        df_in_del.to_excel(writer, index=False, sheet_name="gate+input delays")
        corr_table.to_excel(writer, sheet_name="corr table")
        
    print("spreadsheet with results saved in " + os.getcwd() + "/spreadsheets/" + spreadsheet + ".xlsx")

