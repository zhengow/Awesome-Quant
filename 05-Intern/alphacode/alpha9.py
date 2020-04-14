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
    return pd.DataFrame(xmatrix).rank(pct=True,axis=0).values

''' Constants'''
delay = 1
start_date = str(20100101)
end_date = str(20181231)

histdays = 20 # need histdays >= delay
actdays = get_datelist(start_date,end_date,histdays,-1)

days = [int(d.replace('-', '')) for d in meta_api.get_trading_date_range(int(start_date), int(end_date), 'SSE')]

daysdata = helpfunc_loadcache(actdays[0],actdays[-1],'days')
symbols = helpfunc_loadcache(actdays[0],actdays[-1],'stocks')

instruments = len(symbols)

startdi = daysdata.tolist().index(days[0])
enddi = startdi + len(days) - 1

'Data Part'
ret = helpfunc_loadcache(actdays[0],actdays[-1],'vwapret','basedata')
close = helpfunc_loadcache(actdays[0],actdays[-1],'close','basedata')

groupdata = helpfunc_loadcache(actdays[0],actdays[-1],'WIND01','basedata')

'Alpha Part'
alpha = np.full([1, enddi - startdi + 1, instruments], np.nan)

for ii in range(instruments):
    print(ii)
    sma = np.full([high.shape[0]], np.nan)
    sma[startdi] = ((high[startdi-delay,ii]+low[startdi-delay,ii])/2-(high[startdi-delay,ii]-high[startdi-1-delay,ii]+low[startdi-delay,ii]-low[startdi-1-delay,ii])/2)*(high[startdi-delay,ii]-low[startdi-delay,ii])/volume[startdi-delay,ii]
    alpha[0][0][ii] = sma[startdi]
    for di in range(startdi+1,enddi+1):
        indictor = ((high[di-delay,ii]+low[di-delay,ii])/2-(high[di-delay,ii]-high[di-1-delay,ii]+low[di-delay,ii]-low[di-1-delay,ii])/2)*(high[di-delay,ii]-low[di-delay,ii])/volume[di-delay,ii]
        if(np.isnan(sma[di-1])):
            sma[di] = indictor
        else:
            sma[di] = (sma[di-1]*5+indictor*2)/7
        alpha[0][di-startdi][ii] = sma[di]


        
 
    
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


