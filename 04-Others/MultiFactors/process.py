import pandas as pd
import numpy as np
#3234 rows  3933 cols
#date = pd.read_csv('date.csv')

#alpha1 = np.load("alpha1.npy")
#data = 'vol'
df = pd.read_csv('ret2.csv')
df.rename(columns={'Unnamed: 0':'date'},inplace=True)
i = {'date': a}
df.set_index(df['date'], inplace=True)
del df['date']

#df.drop([len(df)-1], inplace=True)
#del df['3934']
#del df['3933']
#df = pd.read_csv('volume.csv', index_col='date')
#df2 = pd.read_csv('close.csv', index_col='date')
#df.set_index(date['date'], inplace=True)
#df.rename(columns={'0':'inxret'}, inplace=True)
#del df['Unnamed: 0']

df.to_csv('ret2.csv')