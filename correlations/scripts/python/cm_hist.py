import pandas as pd
import math

import config.global_vars as gv

from scripts.python.correlations import correlations
from scripts.python.functions import *

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

# queste due sono da modificare per poter prendere anche più di un ingresso
# def create_HW(len):
#     il = list()
#     x = list()

#     # contiene il risultato della funzione di correlazione usata per a per tutte le sim
#     corr_func_a = list()
#     corr_func_b = list()
#     corr_func_ab = list()

#     for i in range(0, len):
#         s = format(i, '04b')
#         # contiene la lista degli input in formato binario
#         il.append(s)

#     for i in range(len):
#         for j in range(len):
#             post_a = int(il[j][0])
#             post_b = int(il[j][1])
#             corr_func_a.append(post_a)
#             corr_func_b.append(post_b)
#             corr_func_ab.append(my_and(post_a, post_b))

#     x.append(corr_func_a)
#     x.append(corr_func_b)
#     x.append(corr_func_ab)

#     return x

def create_HW(len):
    il = list()

    # corr_func contiene una lista per ogni input
    # ognuna di queste liste contiene l'HW del corrispettivo input per ogni sim
    corr_func = list()
    for i in range(gv.in_size):
        l = list()
        corr_func.append(l)

    for i in range(0, len):
        s = format(i, '04b')
        # contiene la lista degli input in formato binario
        il.append(s)

    for i in range(len):
        for j in range(len):
            for input in range(gv.in_size):
                post = int(il[j][input])
                corr_func[input].append(hw(post))
    
    return corr_func

# def create_HD(len):
#     il = list()
#     x = list()
#     corr_func_a = list()
#     corr_func_b = list()
#     corr_func_ab = list()

#     for i in range(0, len):
#         s = format(i, '04b')
#         il.append(s)

#     for i in range(len):
#         for j in range(len):
#             pre_a = int(il[i][0])
#             post_a = int(il[j][0])
#             pre_b = int(il[i][1])
#             post_b = int(il[j][1])

#             corr_func_a.append(my_xor(pre_a, post_a))
#             corr_func_b.append(my_xor(pre_b, post_b))
#             corr_func_ab.append(
#                                 my_xor(my_and(pre_a, pre_b),
#                                 my_and(post_a, post_b))
#                                 )

#     x.append(corr_func_a)
#     x.append(corr_func_b)
#     x.append(corr_func_ab)

#     return x

def create_HD(len):
    il = list()
    
    corr_func = list()
    for i in range(gv.in_size):
        l = list()
        corr_func.append(l)

    for i in range(0, len):
        s = format(i, '04b')
        il.append(s)

    for i in range(len):
        for j in range(len):
            for input in range(gv.in_size):
                pre = int(il[i][input])
                post = int(il[j][input])
                corr_func[input].append(hd(pre, post))

    return corr_func


# create the correlation matrix and histogram data
def create_cm_hist(logs):

    # creates the list containing the number of toggles for each simulation
    toggles = create_toggle_lists(logs)
    t_df = create_toggles_hist(toggles)

    t_len = math.sqrt(len(toggles[0]))
    
    HW_inputs = create_HW(int(t_len))
    HD_inputs = create_HD(int(t_len))
    
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

    # data = {"HW a": corr_HW[0], "HW b": corr_HW[1], "HW ab": corr_HW[2],
    #                 "HD a": corr_HD[0], "HD b": corr_HD[1], "HD ab": corr_HD[2]}

    df = pd.DataFrame(data=data, index=index)

    return df, t_df[0], t_df[1], t_df[2]
