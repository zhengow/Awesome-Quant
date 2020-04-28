import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data import Data
import math
import time

class BacktestEngine(object):

    """
    This class is used to read data,
    process data to standard form.
    """
    
    def __init__(self, alpha, trade_date):
        
        self.trade_date = trade_date
        self.dailyret = Data.get('ret2', self.trade_date.iloc[0], self.trade_date.iloc[-1])
        self.inxret = Data.get('inxret', self.trade_date.iloc[0], self.trade_date.iloc[-1])
        self.all = Data.get('all', self.trade_date.iloc[0], self.trade_date.iloc[-1])
        #stop = (1-pd.isnull(self.all)).astype(np.bool)
        self.dailyret[pd.isnull(self.all)] = np.nan
        self.trade_days = self.trade_date.shape[0]
        self.cash = np.full([self.trade_days+1],1000000.0)
        self.mktcash = np.full([self.trade_days+1],1000000.0)
        self.posret = np.full([self.trade_days],np.nan)
        self.negret = np.full([self.trade_days],np.nan)
        self.ret = np.full([self.trade_days],np.nan)
        self.shrp = np.full([10],np.nan)
        #dummy = alpha.alpha.copy()
        self.run(alpha)
    
    def run(self, alpha):
        for ii in range(self.trade_days):
            ret = self.dailyret.iloc[ii,:]
            cond = pd.isnull(ret)
            ret[cond] = 0
            pos = alpha[ii,:].copy()
            pos[pos<0] = 0
            pos[pd.isnull(pos)|cond] = 0
            pos = pos/np.sum(pos)
            neg = alpha[ii,:].copy()
            neg[neg>0] = 0
            neg[pd.isnull(neg)|cond] = 0
            neg = -neg/np.sum(neg)
            self.posret[ii] = np.dot(pos, ret)
            self.negret[ii] = np.dot(neg, ret)
            if(np.isnan(self.posret[ii])):
                self.ret[ii] = self.negret[ii]
            if(np.isnan(self.negret[ii])):
                self.ret[ii] = self.posret[ii]
            if( not np.isnan(self.posret[ii]) and not np.isnan(self.negret[ii])):
                self.ret[ii] = (self.posret[ii]+self.negret[ii])/2
            if(np.isnan(self.ret[ii])):
                self.ret[ii] = 0
        
        for ii in range(self.trade_days):
            self.mktcash[ii+1] = self.mktcash[ii]*(1+self.inxret.iloc[ii,0])
            if(np.isnan(self.ret[ii])):
                self.cash[ii+1] = self.cash[ii]
            else:
                self.cash[ii+1] = self.cash[ii]*(1+self.ret[ii])
        
        
    def prints(self):
        len_10 = len(self.ret)//10
        ret_10 = []
        for ii in range(9):
            ret_10.append(self.ret[len_10*ii:len_10*(ii+1)])
        ret_10.append(self.ret[len_10*9:])
        for ii in range(10):
            ret_mean = np.mean(ret_10[ii])
            ret_std = np.std(ret_10[ii])
            IC = ret_mean/ret_std
            self.shrp[ii] = IC*np.sqrt(252)
            print("Year", ii+2010, '.1.1 to', ii+2011, '.1.1 shrp/ret: ', self.shrp[ii], np.sum(ret_10[ii]))
        print("average shrp: ", np.mean(self.shrp[1:]))
        
    def show(self):
        len_10 = len(self.trade_date)//10
        xticks = []
        for ii in range(10):
            xticks.append(self.trade_date.iloc[ii*len_10])
        x = np.arange(len(self.dailyret.index))
        plt.plot(x, self.cash[1:])
        plt.plot(self.mktcash)
        #plt.xticks(xticks)
        plt.show()

class BacktestPerson(BacktestEngine):

    """
    This class is used to read data,
    process data to standard form.
    """
    
    def __init__(self, alpha, trade_date):
        
        self.trade_date = trade_date
        self.symbols = Data.get('symbols', self.trade_date.iloc[0], self.trade_date.iloc[-1])
        self.dailyret = Data.get('ret2', self.trade_date.iloc[0], self.trade_date.iloc[-1])
        self.inxret = Data.get('inxret', self.trade_date.iloc[0], self.trade_date.iloc[-1])
        self.all = Data.get('all', self.trade_date.iloc[0], self.trade_date.iloc[-1])
        #stop = (1-pd.isnull(self.all)).astype(np.bool)
        self.dailyret[pd.isnull(self.all)] = np.nan
        self.trade_days = self.trade_date.shape[0]
        self.stocks = np.full([self.trade_days, 5], '11111111111111')
        self.cash = np.full([self.trade_days+1],1000000.0)
        self.mktcash = np.full([self.trade_days+1],1000000.0)
        self.posret = np.full([self.trade_days],np.nan)
        self.negret = np.full([self.trade_days],np.nan)
        self.ret = np.full([self.trade_days],np.nan)
        self.shrp = np.full([10],np.nan)
        #dummy = alpha.alpha.copy()
        self.run(alpha)
    
    def run(self, alpha):
        for ii in range(self.trade_days):
            idx = np.where(alpha[ii,:]>0)
            self.stocks[ii,:] = self.symbols.iloc[idx[0],0]
            ret = self.dailyret.iloc[ii,:]
            cond = pd.isnull(ret)
            ret[cond] = 0
            pos = alpha[ii,:].copy()
            pos[pos<0] = 0
            pos[pd.isnull(pos)|cond] = 0
            pos = pos/np.sum(pos)
            
            self.posret[ii] = np.dot(pos, ret)
            self.negret[ii] = -self.inxret.iloc[ii,0]*0.1
            if(np.isnan(self.posret[ii])):
                self.ret[ii] = self.negret[ii]
                continue
            if(np.isnan(self.negret[ii])):
                self.ret[ii] = self.posret[ii]
                continue
            self.ret[ii] = (self.posret[ii]+self.negret[ii])/2
        
        for ii in range(self.trade_days):
            self.mktcash[ii+1] = self.mktcash[ii]*(1+self.inxret.iloc[ii,0])
            if(np.isnan(self.ret[ii])):
                self.cash[ii+1] = self.cash[ii]
            else:
                self.cash[ii+1] = self.cash[ii]*(1+self.ret[ii])
        