import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data import Data
import math

class BacktestEngine(object):

    """
    This class is used to read data,
    process data to standard form.
    """
    
    def __init__(self, alpha):
        
        self.trade_date = alpha.trade_date
        self.dailyret = Data.get('ret', self.trade_date.iloc[0], self.trade_date.iloc[-1])
        self.inxret = Data.get('inxret', self.trade_date.iloc[0], self.trade_date.iloc[-1])
        self.trade_days = self.trade_date.shape[0]
        self.cash = np.full([self.trade_days+1],1000000.0)
        self.posret = np.full([self.trade_days],np.nan)
        self.negret = np.full([self.trade_days],np.nan)
        self.ret = np.full([self.trade_days],np.nan)
        self.shrp = np.full([10],np.nan)
        dummy = alpha.alpha.copy()
        self.run(dummy)
    
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
            else:
                self.ret[ii] = (self.posret[ii]+self.negret[ii])/2
        
        for ii in range(self.trade_days):
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
            print("Year ", ii+1, " shrp: ", self.shrp[ii])
        print("average shrp: ", np.mean(self.shrp))
        
    def show(self):
        len_10 = len(self.trade_date)//10
        xticks = []
        for ii in range(10):
            xticks.append(self.trade_date.iloc[ii*len_10])
        plt.plot(self.dailyret.index, self.cash[1:])
        plt.xticks(xticks)
        plt.show()