import config.global_vars as gv

# Computational logic
def my_xor(i1, i2):
	return i1 ^ i2
	
def my_and(i1, i2):
	return i1 & i2

def hw(post):
    return post

def hd(pre, post):
    return my_xor(pre, post)

# consume model working only on the post values of the simulations
def consume_model(post):
    result = list()

    for i in range(gv.in_size):
        l = list()
        result.append(l)

    for i in range(gv.simulations):
        for input in range(gv.in_size):
            result[input].append(hw(post[input][i]))

    return result

# consume model working on the pre and post values of the simulations
def consume_model_pre_post(pre, post):
    result = list()

    for i in range(gv.in_size):
        l = list()
        result.append(l)

    for i in range(gv.simulations):
        for input in range(gv.in_size):
            result[input].append(hd(pre[input][i], post[input][i]))

    return result