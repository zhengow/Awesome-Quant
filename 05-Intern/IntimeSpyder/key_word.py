import pandas as pd
import time

def getkeywords(filename):
    keywords = []
    df = pd.read_csv(filename, encoding='gbk')
    for i in range(df.shape[0]):
        stock = df.iloc[i,0]
        code = stock.split('.')[0]
        stkname = stock.split()[1]
        'clean stock name'
        stkname = cleanStk(stkname)
        keywords.append(code+'+'+stkname)
    return keywords


def cleanStk(stkname):
    if('(' in stkname):
        stkname = stkname.split('(')[0] #tuishi company
    stkname = stkname.lower()
    if('st' in stkname):
        if('*' in stkname):
            tmp = stkname.split('*')[1]
            stkname = tmp + '+' + stkname
        else:
            tmp = '*' + stkname
            stkname = stkname + '+' + tmp
    stkname = stkname.replace('\t','')
    return stkname