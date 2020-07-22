# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 20:43:16 2020

@author: Asus
"""
import tushare as ts
import pandas as pd
import numpy as np
import datetime
import black_scholes as bs
import matplotlib.pyplot as plt

pro = ts.pro_api()

SSE = pro.opt_basic(exchange='SSE')

optionCode = '10002647.SH'
#华泰柏瑞沪深300ETF期权2008认购4.80
Option = pro.opt_daily(ts_code=optionCode)

HS300 = pro.fund_daily(ts_code='510300.SH')

df = pd.DataFrame()
df['date'] = Option['trade_date']
df['C'] = Option['close']
cond = HS300['trade_date']>=df['date'].iloc[-1]
df['S'] = HS300['close'][cond]
df['K'] = 4.8
df['r'] = 0.02
cond2 = SSE.ts_code==optionCode
expiration = SSE.maturity_date[cond2].values[0]
expiration = datetime.datetime.strptime(expiration,'%Y%m%d').date()
#calculate T

df['T'] = 1.00
for ii in range(len(df)):
    cur = datetime.datetime.strptime(df['date'][ii],'%Y%m%d').date()
    df['T'][ii] = ((expiration-cur).days)/360

df['sigma'] = 1.00
for ii in range(len(df)):
    df['sigma'][ii] = bs.blackScholesSolveImpliedVol(df['C'][ii], 'Call', df['S'][ii], df['K'][ii], df['T'][ii], df['r'][ii])

plt.plot(df['date'], df['sigma'])
plt.show()
    









