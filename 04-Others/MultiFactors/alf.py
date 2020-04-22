import numpy as np
import pandas as pd
from data import Data

class Alpha(object):
    
    def __init__(self, start_date, end_date):
        self.trade_date = Data.get('date', start_date, end_date)
        self.start = self.trade_date.iloc[0]
        self.end = self.trade_date.iloc[-1]
        self._init_data()
        self.run()
        
    def run(self):
        '''
        Calculate your alpha here.
        '''
        pass
        
    def Neutralize(self, method):
        print(method)
        if(method == 'test'):
            for ii in range(self.alpha.shape[0]):
                mean = np.nanmean(self.alpha[ii,:])
                self.alpha[ii,:] = self.alpha[ii,:] - mean
            
        if(method == "IND"):
            inds = pd.read_csv('groupdata.csv', index_col='date')
            start = np.where(inds.index == self.start)[0].tolist()[0]
            end = np.where(inds.index == self.end)[0].tolist()[0]
            for di in range(start, end+1):
                series = inds.iloc[di,:]
                for ind in series.unique():
                    cond = (series==ind)
                    mean = np.nanmean(self.alpha[di-start][cond])
                    self.alpha[di-start][cond] = self.alpha[di-start][cond] - mean
            '''
        if(method == "MV"):
            1
        else:
            print("No such Neutralization!!")
            '''
    def Rank(self, data):
        return pd.DataFrame(data).rank(pct=True, axis=1)

class Alphatest(Alpha):
    
    def run(self):
        '''
        Calculate!
        '''
        delay = 0
        #data = self.close.shift(5)-self.close
        data = self.close-self.open
        #data = self.Rank(data)
        
        start = np.where(data.index == self.start)[0].tolist()[0]
        end = np.where(data.index == self.end)[0].tolist()[0]
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self.alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self.Neutralize('IND')
        print("Neutralize is finished!")
        
        
        
    def _init_data(self):
        
        hist = 20

        self.close = Data.get('close', self.start, self.end, hist)
        self.open = Data.get('open', self.start, self.end, hist)
        
        self.alpha = np.full([self.trade_date.shape[0], self.close.shape[1]], np.nan)
        print("init data is finished!")

class Alpha1(Alpha):
    
    def run(self):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        data = self.close.rolling(10).corr(self.vol)
        #data = self.Rank(data)
        
        start = np.where(data.index == self.start)[0].tolist()[0]
        end = np.where(data.index == self.end)[0].tolist()[0]
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self.alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self.Neutralize('IND')
        print("Neutralize is finished!")
        
        
        
    def _init_data(self):
        
        hist = 20

        self.close = Data.get('close', self.start, self.end, hist)
        self.vol = Data.get('volume', self.start, self.end, hist)
        self.vol[self.vol==0] = np.nan
        #self.high = Data.get('high', start, end, hist)
        
        self.alpha = np.full([self.trade_date.shape[0], self.close.shape[1]], np.nan)
        print("init data is finished!")
        
class Alpha2(Alpha):
    
    def run(self):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        data = self.close.rolling(10).corr(self.vol)
        data = self.Rank(data)
        
        start = np.where(data.index == self.start)[0].tolist()[0]
        end = np.where(data.index == self.end)[0].tolist()[0]
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self.alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self.Neutralize('IND')
        print("Neutralize is finished!")
        
        
        
    def _init_data(self):
        
        hist = 20

        self.close = Data.get('close', self.start, self.end, hist)
        self.vol = Data.get('volume', self.start, self.end, hist)
        self.vol[self.vol==0] = np.nan
        #self.high = Data.get('high', start, end, hist)
        
        self.alpha = np.full([self.trade_date.shape[0], self.close.shape[1]], np.nan)
        print("init data is finished!")

class Alpha3(Alpha):
    
    def run(self):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        data = self.amount.rolling(10).std()
        #data = self.Rank(data)
        
        start = np.where(data.index == self.start)[0].tolist()[0]
        end = np.where(data.index == self.end)[0].tolist()[0]
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self.alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self.Neutralize('IND')
        print("Neutralize is finished!")
        
        
        
    def _init_data(self):
        
        hist = 20

        self.amount = Data.get('amount', self.start, self.end, hist)
        
        self.alpha = np.full([self.trade_date.shape[0], self.amount.shape[1]], np.nan)
        print("init data is finished!")