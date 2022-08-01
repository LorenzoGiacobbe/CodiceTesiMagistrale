import config.global_vars as gv

def sel_func(il):
    result = list()

    for i in range(gv.in_size):
        l = list()
        result.append(l)

    for i in range(len(il)):
        for input in range(gv.in_size):
            # selection function
            post = int(il[i][(gv.in_size + gv.rand_size) + input])
            # consume model
            result[input].append(post)

    return result

def sel_func_pre_post(il):
    pre = list()
    post = list()


    for i in range(gv.in_size):
        a = list()
        b = list()
        pre.append(a)
        post.append(b)


    for i in range(len(il)):
        for input in range(gv.in_size):
            # selection function
            pre[input].append(int(il[i][input]))
            post[input].append(int(il[i][(gv.in_size + gv.rand_size) + input]))

    return pre, post