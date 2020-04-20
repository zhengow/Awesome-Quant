import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class BacktestEngine(object):

    """
    This class is used to read data,
    process data to standard form.
    """
    
    def __init__(self, start_date, end_date):

        self.trade_date = self.get_trade_date()
        self.dailyret = self.load_dailyret(self.trade_date.index[0],self.trade_date.index[-1])
        self.inxret = self.load_inxret(self.trade_date.index[0],self.trade_date.index[-1])
        self.trade_days = self.trade_date.shape[0]
        self.cash = np.full([self.trade_days+1],1000000)
        self.posret = np.full([self.trade_days],np.nan)
        self.negret = np.full([self.trade_days],np.nan)
        self.ret = np.full([self.trade_days],np.nan)
    
    def get_trade_date(self, start_date, end_date):
        
        date = pd.read_csv('date.csv')
        return date.loc[start_date:end_date,:]
    
    
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

    def run(self):
        for ii in range(self.days):
            if(np.sum(self.alpha.iloc[ii,:]>1e7)):
                print("The alpha of ", ii, " is too large!")
            ret = self.dailyret.iloc[ii,:]
            cond = pd.isnull(ret)
            ret[cond] = 0
            pos = self.alpha.iloc[ii,:]
            pos[pos<0] = 0
            pos[pd.isnull(pos)|cond] = 0
            pos = pos/np.sum(pos)
            neg = self.alpha.iloc[ii,:]
            neg[neg>0] = 0
            neg[pd.isnull(neg)|cond] = 0
            neg = -neg/np.sum(neg)
            self.posret[ii] = np.dot(pos, ret)
            self.negret[ii] = np.dot(neg, ret)
            self.ret[ii] = (self.posret[ii]+self.negret[ii])/2
        
        for ii in range(self.days):
            self.cash[ii+1] = self.cash[ii]*self.ret[ii]
        
        
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