from scripts.python.logic import *
import config.global_vars as gv

def hw(post):
    return post

def hd(pre, post):
    return my_xor(pre, post)

def consume_model(post):
    result = list()

    for i in range(gv.in_size):
        l = list()
        result.append(l)

    for i in range(len(post)):
        for input in range(gv.in_size):
            # consume model
            result[input].append(hw(post[input][i]))
    return result

def consume_model_pre_post(pre, post):
    result = list()

    for i in range(gv.in_size):
        l = list()
        result.append(l)

    for i in range(len(post)):
        for input in range(gv.in_size):
            # consume model
            result[input].append(hd(pre[input][i], post[input][i]))
    return result