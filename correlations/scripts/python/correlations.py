import pandas as pd
import config.global_vars as gv

# takes as inputs the two lists between wich the correlation needs to be calculated
# (i.e. the toggle list and the list generated through sel_func and consume_model)
def pearsons_correlation(toggles, inputs):
    df = pd.concat([pd.DataFrame(inputs), pd.DataFrame(toggles[0])], axis=1)
    corr_table = df.corr(method='pearson')

    df = pd.concat([pd.DataFrame(inputs), pd.DataFrame(toggles[1])], axis=1)
    corr_table_del = df.corr(method='pearson')

    df = pd.concat([pd.DataFrame(inputs), pd.DataFrame(toggles[2])], axis=1)
    corr_table_in_del = df.corr(method='pearson')

    return corr_table, corr_table_del, corr_table_in_del

def correlations(toggles, inputs):
    corr = list()
    for i in range(gv.in_size):
        l = list()
        corr.append(l)

        # contains for input i the correlations for the 3 delays
        # correlations[0] -> correlation without delays
        # correlations[1] -> correlation with gate delay
        # correlations[2] -> correlation with gate and input delay
        correlations = pearsons_correlation(toggles, inputs[i])
        for j in range(3):
            corr[i].append(correlations[j].iat[0, 1])

    return corr