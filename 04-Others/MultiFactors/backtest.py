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
    
    def __init__(self, alpha, trade_date, name):
        self.name = name
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
        self.shrp = np.full([11],np.nan)
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
        idx = [242,486,729,967,1212,1456,1700,1944,2187,2431]
        print(self.name)
        ret_11 = []
        ret_11.append(self.ret[:idx[0]])
        for ii in range(9):
            ret_11.append(self.ret[idx[ii]:idx[ii+1]])
        ret_11.append(self.ret[idx[-1]:])
        for ii in range(10):
            ret_mean = np.nanmean(ret_11[ii])
            ret_std = np.nanstd(ret_11[ii])
            IC = ret_mean/ret_std
            self.shrp[ii] = IC*np.sqrt(252)
            print("%d.1.1 to %d.1.1 shrp/ret: %2.4f / %2.4f%%"%(ii+2010,ii+2011,self.shrp[ii], 100*np.nansum(ret_11[ii])))
        ret_mean = np.nanmean(ret_11[-1])
        ret_std = np.nanstd(ret_11[-1])
        IC = ret_mean/ret_std
        self.shrp[-1] = IC*np.sqrt(252)
        print("%d.1.1 to %d.4.1 shrp/ret: %2.4f / %2.4f%%"%(2020,2020,self.shrp[-1], 100*252*np.nanmean(ret_11[-1])))
        shrp = np.nanmean(self.ret)/np.nanstd(self.ret)*np.sqrt(252)
        print("average shrp: %2.4f" % shrp)
        print("average return: %2.4f%%" % (100*np.nanmean(self.ret)*252))
        
    def show(self):
        #len_10 = len(self.trade_date)//10
        locs = np.linspace(1,len(self.trade_date)-1,num=5,endpoint=True,dtype=int)
        labels=[]
        for ii in locs:
            labels.append(self.trade_date.iloc[ii])
        x = np.arange(len(self.dailyret.index))
        p1, = plt.plot(x, self.cash[1:])
        p2, = plt.plot(self.mktcash)
        plt.legend([p1, p2],[self.name, "Market:inx500"])
        plt.xticks(locs,(labels))
        plt.show()

class BacktestML(BacktestEngine):

    """
    This class is used to read data,
    process data to standard form.
    """
    def prints(self):
        idx = [242,486,729,967,1212,1456,1700,1944,2187,2431]
        print(self.name)
        ret_11 = []
        ret_11.append(self.ret[:idx[0]])
        for ii in range(9):
            ret_11.append(self.ret[idx[ii]:idx[ii+1]])
        ret_11.append(self.ret[idx[-1]:])
        for ii in range(1):
            ret_mean = np.nanmean(ret_11[ii])
            ret_std = np.nanstd(ret_11[ii])
            IC = ret_mean/ret_std
            self.shrp[ii] = IC*np.sqrt(252)
            print("%d.1.1 to %d.1.1(InSample) shrp/ret: %2.4f / %2.4f%%"%(ii+2010,ii+2011,self.shrp[ii], 100*np.nansum(ret_11[ii])))
        for ii in range(1,10):
            ret_mean = np.nanmean(ret_11[ii])
            ret_std = np.nanstd(ret_11[ii])
            IC = ret_mean/ret_std
            self.shrp[ii] = IC*np.sqrt(252)
            print("%d.1.1 to %d.1.1(OutSample) shrp/ret: %2.4f / %2.4f%%"%(ii+2010,ii+2011,self.shrp[ii], 100*np.nansum(ret_11[ii])))
        ret_mean = np.nanmean(ret_11[-1])
        ret_std = np.nanstd(ret_11[-1])
        IC = ret_mean/ret_std
        self.shrp[-1] = IC*np.sqrt(252)
        print("%d.1.1 to %d.4.1(OutSample) shrp/ret: %2.4f / %2.4f%%"%(2020,2020,self.shrp[-1], 100*252*np.nanmean(ret_11[-1])))
        shrp = np.nanmean(self.ret[250:])/np.nanstd(self.ret[250:])*np.sqrt(252)
        print("average shrp(Out Sample): %2.4f" % shrp)
        print("average return(Out Sample): %2.4f%%" % (100*np.nanmean(self.ret[250:])*252))
    
    def prints2(self):
        print(self.name)
        len_10 = len(self.ret)//10
        ret_10 = []
        for ii in range(9):
            ret_10.append(self.ret[len_10*ii:len_10*(ii+1)])
        ret_10.append(self.ret[len_10*9:])
        for ii in range(1):
            ret_mean = np.nanmean(ret_10[ii])
            ret_std = np.nanstd(ret_10[ii])
            IC = ret_mean/ret_std
            self.shrp[ii] = IC*np.sqrt(252)
        print("average shrp(In Sample): %2.4f" % self.shrp[0])
        print("average return(In Sample): %2.4f%%" % (100*np.nansum(ret_10[0])))
        
        for ii in range(1,10):
            ret_mean = np.nanmean(ret_10[ii])
            ret_std = np.nanstd(ret_10[ii])
            IC = ret_mean/ret_std
            self.shrp[ii] = IC*np.sqrt(252)

        shrp = np.nanmean(self.ret[250:])/np.nanstd(self.ret[250:])*np.sqrt(252)
        print("average shrp(Out Sample): %2.4f" % shrp)
        print("average return(Out Sample): %2.4f%%" % (100*np.nanmean(self.ret[250:])*252))
        
    
    def show(self):
        cash = np.full([self.trade_days+1],1000000.0)
        mktcash = np.full([self.trade_days+1],1000000.0)
        window = 250
        for ii in range(self.trade_days-window):
            mktcash[ii+window+1] = mktcash[ii+window]*(1+self.inxret.iloc[ii+window,0])
            if(np.isnan(self.ret[ii+window])):
                cash[window+ii+1] = cash[ii+window]
            else:
                cash[window+ii+1] = cash[ii+window]*(1+self.ret[ii+window])
        #len_10 = len(self.trade_date)//10
        locs = np.linspace(window,len(self.trade_date)-1,num=5,endpoint=True,dtype=int)
        labels=[]
        for ii in locs:
            labels.append(self.trade_date.iloc[ii])
        locs = np.linspace(1,len(self.trade_date)-window-1,num=5,endpoint=True,dtype=int)
        #x = np.arange(len(self.dailyret.index)-window)
        p1, = plt.plot(cash[window:])
        p2, = plt.plot(mktcash[window:])
        plt.legend([p1, p2],[self.name, "Market:inx500"])
        plt.xticks(locs,(labels))
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
            #print("idx:",idx[0])
            if(len(idx[0])>0):
                self.stocks[ii,:] = self.symbols.iloc[idx[0],0]
            ret = self.dailyret.iloc[ii,:]
            cond = pd.isnull(ret)
            ret[cond] = 0
            pos = alpha[ii,:].copy()
            pos[pos<0] = 0
            pos[pd.isnull(pos)|cond] = 0
            pos = pos/np.sum(pos)
            
            self.posret[ii] = np.dot(pos, ret)
            #self.negret[ii] = -self.inxret.iloc[ii,0]*0.1
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
                if(ii%5==0):
                    self.cash[ii+1] = self.cash[ii]*(1+self.ret[ii]-0.0015)
                else:
                    self.cash[ii+1] = self.cash[ii]*(1+self.ret[ii])