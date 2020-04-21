import numpy as np
import pandas as pd
from data import Data

class Alpha(object):
    
    def __init__(self, start_date, end_date):
        #self.trade_date = Date.get('date', start_date, end_date)
        #self._init_data()
        #self.run()
        pass
    
        
    def run(self):
        '''
        Calculate your alpha here.
        '''
        pass
    
    def get(self):
        return self.alpha
        
    def Neutralize(self, method):
        
        for ii in range(self.alpha.shape[0]):
            mean = np.nanmean(self.alpha[ii,:])
            self.alpha[ii,:] = self.alpha[ii,:]-mean
            print(self.alpha[ii,:5])
            '''
        if(method == "IND"):
            1
        if(method == "MV"):
            1
        else:
            print("No such Neutralization!!")
            '''
    def Rank(self):
        return pd.DataFrame(self.alpha).rank(pct=True, axis=1)

class Alpha1(Alpha):
    
    def __init__(self, start_date, end_date):
        print("child")
        self.trade_date = Data.get('date', start_date, end_date)
        self.start = self.trade_date.iloc[0]
        self.end = self.trade_date.iloc[-1]
        self._init_data()
        self.run()
    
    def run(self):
        '''
        Calculate!
        '''
        delay = 1
        
        data = self.close
        start = np.where(data.index == self.start)[0].tolist()[0]
        end = np.where(data.index == self.end)[0].tolist()[0]
        for di in range(start, end):
            self.alpha[di-start,:] = data.iloc[di-delay,:]
        
        self.alpha = self.Neutralize('test')
        
        print("Alpha is finished!")
        
        
    def _init_data(self):
        hist = 10

        self.close = Data.get('close', self.start, self.end, hist)
        #self.high = Data.get('high', start, end, hist)
        
        self.alpha = np.full([self.trade_date.shape[0], self.close.shape[1]], np.nan)
        
        