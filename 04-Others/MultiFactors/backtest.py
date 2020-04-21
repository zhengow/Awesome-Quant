import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data import Data

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
        self.cash = np.full([self.trade_days+1],1000000)
        self.posret = np.full([self.trade_days],np.nan)
        self.negret = np.full([self.trade_days],np.nan)
        self.ret = np.full([self.trade_days],np.nan)
        dummy = alpha.alpha.copy()
        self.run(dummy)

    '''
    def get_trade_date(self, start_date, end_date):
        
        date = pd.read_csv('date.csv')
        start = alpha.index[0]
        end = alpha.index[-1]
        return date.loc[start:end_date,:]

    def load_inxret(self, start, end):
        inxret = pd.read_csv('inxret.csv')
        return inxret.loc[start:end,:]
    
    def load_dailyret(self, start, end):

        ret = pd.read_csv('ret.csv')
        return ret.loc[start:end,:]

    def load_alpha(self, alpha):
        if(alpha.shape[0]!=self.ret.shape[0]):
            print("Wrong size!")
        else:
            self.alpha = alpha
    '''
    
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
            self.ret[ii] = (self.posret[ii]+self.negret[ii])/2
        '''
        for ii in range(self.trade_days):
            print(ii)
            self.cash[ii+1] = self.cash[ii]*self.ret[ii]
        '''
        
    def prints(self):
        ret_mean = np.mean(self.ret)
        ret_std = np.std(self.ret)
        IC = ret_mean/ret_std
        shrp = IC*np.sqrt(252)
        
        print("shrp: ", shrp)
        

    def show(self):
        x = self.dailyret.index
        y = self.cash[1:]
        plt.plot(x,y)
        plt.show()