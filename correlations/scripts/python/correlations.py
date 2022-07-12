import pandas as pd

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