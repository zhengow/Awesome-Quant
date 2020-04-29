import pandas as pd

symbol = pd.read_csv('symbols.csv', header = None)

idx = []

for item in banklist['ts_code']:
    code = item[:6]
    for ii in range(symbol.shape[0]):
        if(code in symbol['symbol'][ii]):
            idx.append(ii)
            break

high = pd.DataFrame()
low = pd.DataFrame()
high.set_index(alhigh['date'], inplace=True)
low.set_index(alhigh['date'], inplace=True)
alhigh = pd.read_csv('high.csv', index_col = 'date')
allow = pd.read_csv('low.csv', index_col = 'date')