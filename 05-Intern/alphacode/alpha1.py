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

def cal_corr(A,B):

    # Rowwise mean of input arrays & subtract from input arrays themeselves
    A = A.transpose()
    B = B.transpose()
    A_mA = A - A.mean(1)[:,None]
    B_mB = B - B.mean(1)[:,None]
    # Sum of squares across rows
    ssA = (A_mA**2).sum(1);
    ssB = (B_mB**2).sum(1);
    
    # Finally get corr coeff
    tmp = np.dot(A_mA,B_mB.T)/np.sqrt(np.dot(ssA[:,None],ssB[None]))
    corr = np.ones(A.shape[0])
    for i in range(A.shape[0]):
        corr[i] = tmp[i,i]
    return corr

''' Constants'''
delay = 1
start_date = str(20100101)
end_date = str(20181231)

factor_columns = ['5dr_close','5dr_open']

histdays = 10 # need histdays >= delay
actdays = get_datelist(start_date,end_date,histdays,-1)

days = [int(d.replace('-', '')) for d in meta_api.get_trading_date_range(int(start_date), int(end_date), 'SSE')]

daysdata = helpfunc_loadcache(actdays[0],actdays[-1],'days')
symbols = helpfunc_loadcache(actdays[0],actdays[-1],'stocks')

instruments = len(symbols)

startdi = daysdata.tolist().index(days[0])
enddi = startdi + len(days) - 1

'Data Part'
volume = helpfunc_loadcache(actdays[0],actdays[-1],'vol','basedata')
index = np.argwhere(volume == 0) 
for item in index:
    volume[item[0],item[1]]=np.nan
lnvol = np.log(volume)

close = helpfunc_loadcache(actdays[0],actdays[-1],'close','basedata')
ops = helpfunc_loadcache(actdays[0],actdays[-1],'open','basedata')
groupdata = helpfunc_loadcache(actdays[0],actdays[-1],'WIND01','basedata')

alpha = np.full([1, enddi - startdi + 1, instruments], np.nan)

'Alpha Part'
for di in range(startdi,enddi+1):
    'start =time.time()'
    dlnvol = lnvol[di-6:di,:]-lnvol[di-7:di-1,:]
    co = (close[di-6:di,:] - ops[di-6:di,:])/ops[di-6:di,:]
    volRank = []
    coRank = []
    'print("1:",time.time()-start)'
    'start =time.time()'
    for jj in range(6):
        ser = pd.Series(dlnvol[jj,:].tolist())
        volRank.append(ser.rank())
        ser = pd.Series(co[jj,:].tolist())
        coRank.append(ser.rank())
    corr = np.ones(instruments)
    volRank = np.array(volRank)
    coRank = np.array(coRank)
    'print("2:",time.time()-start)'
    'start =time.time()'
    corr = cal_corr(volRank,coRank)
    'print("3:",time.time()-start)'
    'start = time.time()'
    for ii in range(instruments):
        alpha[0][di-startdi][ii] = -1*corr[ii]
    'print("4:",time.time()-start)'
    

    
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



