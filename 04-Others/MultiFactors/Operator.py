import numpy as np
import pandas as pd
from data import Data
class Op(object):
    
    def __init__(self):
        pass
    
    def Neutralize(method, alpha, start = 0, end = 0):
        print(method)
        if(method == 'test'):
            for ii in range(alpha.shape[0]):
                mean = np.nanmean(alpha[ii,:])
                alpha[ii,:] = alpha[ii,:] - mean
            
        if(method == "IND"):
            inds = pd.read_csv('groupdata.csv', index_col='date')
            for di in range(start, end+1):
                series = inds.iloc[di,:]
                for ind in series.unique():
                    cond = (series==ind)
                    mean = np.nanmean(alpha[di-start][cond])
                    alpha[di-start][cond] = alpha[di-start][cond] - mean
            '''
        if(method == "MV"):
            1
        else:
            print("No such Neutralization!!")
            '''
        return alpha
    
    def personalize(data):
        alpha = np.full([data.shape[0], data.shape[1]], np.nan)
        for di in range(data.shape[0]):
            tmp = data[di,:]
            tmp[pd.isnull(tmp)] = -10
            idx = np.argpartition(tmp, -5)[-5:]
            if(di%5==0):
                for ii in idx:
                    alpha[di,ii] = tmp[ii]
            else:
                alpha[di,:] = alpha[di-1,:]
        
        return alpha
    
    def trend(data, startdate, enddate):
        alpha = data
        inx = Data.get('inx500', startdate, enddate, hist = 120)
        #inx = inx.iloc[start:end, :]
        trend = inx.rolling(5).mean()-inx.rolling(10).mean()*1.01
        start = np.where(trend.index == startdate)[0].tolist()[0]
        end = np.where(trend.index == enddate)[0].tolist()[0]
        for di in range(alpha.shape[0]):
            if(trend.iloc[start+di-1,0]<0):
                alpha[di,:] = np.nan
        return alpha, trend
        
    def rank_col(data):
        return pd.DataFrame(data).rank(pct=True, axis=1)
    def rank_row(data):
        return pd.DataFrame(data).rank(pct=True, axis=0)
    def tsrank(data, window):
        rank = data.copy()
        rank.iloc[:window-1,:] = np.nan
        for ii in range(window, data.shape[0]+1):
            tmp = data.iloc[ii-window:ii,:]
            rank.iloc[ii-1,:] = Op.rank_row(tmp).iloc[-1]
        return rank