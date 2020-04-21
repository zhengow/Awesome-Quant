import numpy as np
import pandas as pd
from data import Data

class Alpha(object):
    
    def __init__(self, start_date, end_date):
        print("father")
        self.trade_date = Date.get('date', start_date, end_date)
        self._init_data()
        #self.run()
    
    def _init_data(self):
        pass
        
    def run(self):
        '''
        Calculate your alpha here.
        '''
        pass
    
    def get(self):
        return self.alpha
        
    def Neutralize(self, method):
        if(method == "IND"):
            1
        if(method == "MV"):
            1
        else:
            print("No such Neutralization!!")
    
    def Rank(self):
        return pd.DataFrame(self.alpha).rank(pct=True, axis=1)

class Alpha1(Alpha):
    
    def __init__(self, start_date, end_date):
        print("child")
        self.trade_date = Date.get('date', start_date, end_date)
        self._init_data()
        self.run()
    
    def run(self):
        '''
        Calculate!
        '''
        delay = 1
        
        data = self.close
        
        for di in range(self.start, self.end):
            self.alpha[di-self.start,:] = data.iloc[di-delay,:]
        
        
    def _init_data(self):
        
        hist = 10
        start = self.trade_date.iloc[0]
        end = self.trade_date.iloc[-1]
        self.close = Data.get('close', start, end, hist)
        #self.high = Data.get('high', start, end, hist)

        self.alpha = np.full([self.trade_date.shape[0], self.close.shape[1]], np.nan)
        
        