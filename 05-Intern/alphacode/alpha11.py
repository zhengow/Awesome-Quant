import pandas as pd
import numpy as np
import time
import datetime,requests
from my.data import meta_api, config, quote, my_types
from my.data.daily_factor_generate import StockEvGenerateFactor
from my.data.factor_cache import helpfunc_loadcache

def get_datelist(begT, endT, dback=0, dnext=0):
    days = [int(d.replace('-', '')) for d in meta_api.get_trading_date_range(int(begT), int(endT), 'SSE')]
    dates = [int(d.replace('-', '')) for d in meta_api.get_trading_date_range(int(begT) - 40000, int(endT), 'SSE')]
    days = dates[len(dates) - len(days) - dback:len(dates)+dnext]
    actdays = np.array([int(d) for d in days])

    return actdays

def Rankop_rank(xmatrix):
    return pd.DataFrame(xmatrix).rank(pct=True,axis=1).values

''' Constants'''
delay = 1
start_date = str(20100101)
end_date = str(20181231)

histdays = 20 # need histdays >= delay
actdays = get_datelist(start_date,end_date,histdays,-1)#trading day + hist

days = [int(d.replace('-', '')) for d in meta_api.get_trading_date_range(int(start_date), int(end_date), 'SSE')]
#days is just trading day from start to end

daysdata = helpfunc_loadcache(actdays[0],actdays[-1],'days')
#trading day + hist

symbols = helpfunc_loadcache(actdays[0],actdays[-1],'stocks')

instruments = len(symbols)

startdi = daysdata.tolist().index(days[0])
#find first day
enddi = startdi + len(days) - 1

'Data Part'
volume = helpfunc_loadcache(actdays[0],actdays[-1],'vol','basedata')
index = np.argwhere(volume == 0) 
for item in index:
    volume[item[0],item[1]]=np.nan
close = helpfunc_loadcache(actdays[0],actdays[-1],'close','basedata')
high = helpfunc_loadcache(actdays[0],actdays[-1],'high','basedata')
low = helpfunc_loadcache(actdays[0],actdays[-1],'low','basedata')

groupdata = helpfunc_loadcache(actdays[0],actdays[-1],'WIND01','basedata')

'Alpha Part'
alpha = np.full([1, enddi - startdi + 1, instruments], np.nan)


for di in range(startdi,enddi+1):
    print(di)
    for ii in range(instruments):
        close6 = close[di-6:di,ii]
        low6 = low[di-6:di,ii]
        high6 = high[di-6:di,ii]
        volume6 = volume[di-6:di,ii]
        data = (close6-low6)-(high6-close6)/(high6-low6)*volume6
        
        alpha[0][di-startdi][ii] = sum(data)
    
    

 

'Other Part'
from my.operator import IndNeutralize
alpha[0] = IndNeutralize(alpha[0],groupdata[startdi-1:enddi])
#alpha[1] = IndNeutralize(alpha[1],groupdata[startdi-1:enddi])

#local backtesting
from my_factor.factor import localsimulator2
x = [ str(i) for i in range(alpha.shape[0])]
pnlroute = './pnl/sample'
log = localsimulator2.simu(alpha.copy(),start_date,end_date,pnlroute,x)
from my_factor.factor import summary
pnlfiles = []
for pnl in x:
    pnlfiles.append('./pnl/sample_'+pnl)
    simres = summary.simsummary('./pnl/sample_'+pnl)
##correlation
from my_factor.factor import localcorrelation
try:
    corres = localcorrelation.bcorsummary(pnlfiles)
except:
    localcorrelation.rm_shm_pnl_dep()
    corres = localcorrelation.bcorsummary(pnlfiles)
