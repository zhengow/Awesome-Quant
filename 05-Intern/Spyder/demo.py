from get_index import BaiduIndex
import numpy as np
import pandas as pd

def get_keywords(start):
    keywords = []
    filename = "stockname.csv"
    df = pd.read_csv(filename)
    totalLen = df.shape[0]
    if start>totalLen:
        return keywords
    'for i in range(df.shape[0]):'
    for i in range(10):
        if(i+start>totalLen):
            break
        tmp = df.iloc[i+start,0].split('.')
        code = tmp[0]
        stkname = tmp[1].split(' ')[1]
        'clean stock name'
        if('(' in stkname):
            stkname = stkname.split('(')[0]
        stkname = stkname.lower()
        if('st' in stkname):
            if('*' in stkname):
                tmp = stkname.split('*')[1]
                stkname = tmp + '+' + stkname
            else:
                tmp = '*' + stkname
                stkname = stkname + '+' + tmp
        keywords.append(code+'+'+stkname)
    return keywords

if __name__ == "__main__":
    'if i want to write ith file, i = i-1, start = i*10'
    start = 1870
    keywords = get_keywords(start)

    i = 187
    while(keywords and i<200):
        print(i)
        i = i + 1
        start_time = '2011-01-01'
        end_time = '2020-04-01'

        'create a res_dataframe'
        date_index = pd.date_range(start_time, end_time)
        resDf = pd.DataFrame(index=date_index,columns=keywords)

        baidu_index = BaiduIndex(keywords, start_time, end_time)

        for index in baidu_index.get_index():
            'print(index)'
            for item in keywords:
                if(index['keyword'] in item):
                    resDf.loc[index['date'], item] = index['index']
                    break

        resDf.to_csv('./index/stkindex_'+str(i)+'.csv')
        start = start + 10
        keywords = get_keywords(start)
