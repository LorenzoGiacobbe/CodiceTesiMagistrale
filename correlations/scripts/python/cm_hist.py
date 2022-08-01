import pandas as pd

import config.global_vars as gv

from scripts.python.correlations import correlations
from scripts.python.consume_models import consume_model, consume_model_pre_post, hw, hd
from scripts.python.selection_functions import sel_func, sel_func_pre_post

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

def create_il(in_len):
    il = list()
    len = 0
    f = '0' + str(2*in_len) + 'b'
    
    with open("./logs/inputs.txt", "r") as inputs:
        for line in inputs:
            len += 1
            num = int(line.split()[0])*pow(2, in_len)+int(line.split()[1])
            s = format(num, f)
            il.append(s)

    return il

def create_post(in_len):
    il = create_il(in_len)

    post = sel_func(il)
    result = consume_model(post)

    return result

def create_pre_post(in_len):
    il = create_il(in_len)

    inputs = sel_func_pre_post(il)
    result = consume_model_pre_post(inputs[0], inputs[1])

    return result

# create the correlation matrix and histogram data
def create_cm_hist(logs):

    # creates the list containing the number of toggles for each simulation
    toggles = create_toggle_lists(logs)
    t_df = create_toggles_hist(toggles)

    t_len = gv.in_size + gv.rand_size
    
    # HW_inputs = create_HW(int(t_len))
    # HD_inputs = create_HD(int(t_len))

    HW_inputs = create_post(int(t_len))
    HD_inputs = create_pre_post(int(t_len))

    corr_HW = correlations(toggles, HW_inputs)
    corr_HD = correlations(toggles, HD_inputs)

    index = ["no delays", "gate delays", "gate+inputs delay"]
    data = dict()
    for i in range(gv.in_size):
        key = "HW input" + str(i)
        data[key] = corr_HW[i]
        
    for i in range(gv.in_size):      
        key = "HD input" + str(i)
        data[key] = corr_HD[i]

    df = pd.DataFrame(data=data, index=index)

    return df, t_df[0], t_df[1], t_df[2]
