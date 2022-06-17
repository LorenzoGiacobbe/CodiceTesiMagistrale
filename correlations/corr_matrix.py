import pandas as pd
import subprocess
import sys
import math


# Error handling
def check_code(code):
	if code != 1:
		sim_error()
		sys.exit()

def sim_error():
    	print("Something went wrong with the execution")

def write_chart(writer, sheet, shape):
    workbook  = writer.book
    worksheet = writer.sheets[sheet]
    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({'values': [sheet, 1, 1, shape[0], 1]})
    worksheet.insert_chart(1, 3, chart)

# Write data to excek file
def write_excel(data):
    # data[0] -> correlation matrix
    # data[1] -> data for no del toggle bar chart
    # data[2] -> data for  del toggle bar chart
    # data[3] -> data for in_del toggle bar chart

    with pd.ExcelWriter("./spreadsheets/" + spreadsheet + ".xlsx") as writer:
        # correlation matrix on first sheet
        data[0].to_excel(writer, index=True, sheet_name="Correlation matrix")

        # no del toggles bar chart
        data[1].to_excel(writer, index=True, sheet_name="Toggles no del")
        write_chart(writer, "Toggles no del", data[1].shape)

        # no del toggles bar chart
        data[2].to_excel(writer, index=True, sheet_name="Toggles del")
        write_chart(writer, "Toggles del", data[2].shape)

        # no del toggles bar chart
        data[3].to_excel(writer, index=True, sheet_name="Toggles input del")
        write_chart(writer, "Toggles input del", data[3].shape)

# Computational logic
def my_xor(i1, i2):
	return i1 ^ i2
	
def my_and(i1, i2):
	return i1 & i2

# gadget simulation
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

# Toggle lists creation
def create_toggle_list(log):
	tl = list()

	with open(log) as log:
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

def create_toggle_lists(logs):
    toggle_lists = list()

    for log in logs:
        tl = create_toggle_list(log)
        toggle_lists.append(tl)

    return toggle_lists

def create_HW(len):
    il = list()
    x = list()
    corr_func_a = list()
    corr_func_b = list()
    corr_func_ab = list()

    for i in range(0, len):
        s = format(i, '04b')
        il.append(s)

    for i in range(len):
        for j in range(len):
            post_a = int(il[j][0])
            post_b = int(il[j][1])
            corr_func_a.append(post_a)
            corr_func_b.append(post_b)
            corr_func_ab.append(my_and(post_a, post_b))

    x.append(corr_func_a)
    x.append(corr_func_b)
    x.append(corr_func_ab)

    return x

def create_HD(len):
    il = list()
    x = list()
    corr_func_a = list()
    corr_func_b = list()
    corr_func_ab = list()

    for i in range(0, len):
        s = format(i, '04b')
        il.append(s)

    for i in range(len):
        for j in range(len):
            pre_a = int(il[i][0])
            post_a = int(il[j][0])
            pre_b = int(il[i][1])
            post_b = int(il[j][1])

            corr_func_a.append(my_xor(pre_a, post_a))
            corr_func_b.append(my_xor(pre_b, post_b))
            corr_func_ab.append(
                                my_xor(my_and(pre_a, pre_b),
                                my_and(post_a, post_b))
                                )

    x.append(corr_func_a)
    x.append(corr_func_b)
    x.append(corr_func_ab)

    return x

def pearsons_correlation(toggles, inputs):
    df = pd.concat([pd.DataFrame(inputs), pd.DataFrame(toggles[0])], axis=1)
    corr_table = df.corr(method='pearson')

    df = pd.concat([pd.DataFrame(inputs), pd.DataFrame(toggles[1])], axis=1)
    corr_table_del = df.corr(method='pearson')

    df = pd.concat([pd.DataFrame(inputs), pd.DataFrame(toggles[2])], axis=1)
    corr_table_in_del = df.corr(method='pearson')

    return corr_table, corr_table_del, corr_table_in_del

def correlations(toggles, inputs):
    corr_a = list()
    corr_b = list()
    corr_ab = list()

    correlations_a  = pearsons_correlation(toggles, inputs[0])
    correlations_b  = pearsons_correlation(toggles, inputs[1])
    correlations_ab = pearsons_correlation(toggles, inputs[2])

    for i in range(3):
        corr_a.append(correlations_a[i].iat[0, 1])
        corr_b.append(correlations_b[i].iat[0, 1])
        corr_ab.append(correlations_ab[i].iat[0, 1])

    return corr_a, corr_b, corr_ab

def create_toggles_hist(toggles):
    data = {}
    data_del = {}
    data_in_del = {}

    for e in toggles[0]:
        if e in data:
            val = data.get(e)
            data.update({e: val+1})
        else:
            data.update({e: 1})
    
    for e in toggles[1]:
        if e in data_del:
            val = data_del.get(e)
            data_del.update({e: val+1})
        else:
            data_del.update({e: 1})
    
    for e in toggles[2]:
        if e in data_in_del:
            val = data_in_del.get(e)
            data_in_del.update({e: val+1})
        else:
            data_in_del.update({e: 1})


    p = pd.DataFrame(data.values(), columns=["Toggles"])

    p_del = pd.DataFrame(data_del.values(), columns=["Toggles"])

    p_in_del = pd.DataFrame(data_in_del.values(), columns=["Toggles"])

    return p, p_del, p_in_del


# create the correlation matrix and histogram data
def create_cm_hist(logs):

    toggles = create_toggle_lists(logs)
    t_df = create_toggles_hist(toggles)

    t_len = math.sqrt(len(toggles[0]))
    
    HW_inputs = create_HW(int(t_len))
    HD_inputs = create_HD(int(t_len))
    
    corr_HW = correlations(toggles, HW_inputs)
    corr_HD = correlations(toggles, HD_inputs)

    index = ["no delays", "gate delays", "gate+inputs delay"]
    data = {"HW a": corr_HW[0], "HW b": corr_HW[1], "HW ab": corr_HW[2],
                     "HD a": corr_HD[0], "HD b": corr_HD[1], "HD ab": corr_HD[2]}

    df = pd.DataFrame(data=data, index=index)

    return df, t_df[0], t_df[1], t_df[2]

if __name__ == "__main__": 

    tb = "./verilog/tb/correlation_tb.v"
    spreadsheet = sys.argv[1]

    vvp_logs = simulate(tb)

    data = create_cm_hist(vvp_logs)
    
    write_excel(data)

        