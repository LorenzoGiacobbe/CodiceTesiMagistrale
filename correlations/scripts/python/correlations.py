import pandas as pd
import config.global_vars as gv

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

        # contiene per input i le correlazioni per i 3 ritardi
        # correlations[0] -> corr senza ritardi
        # correlations[1] -> corr gate delay
        # correlations[2] -> corr gate + input delay
        correlations = pearsons_correlation(toggles, inputs[i])
        for j in range(3):
            corr[i].append(correlations[j].iat[0, 1])

    return corr