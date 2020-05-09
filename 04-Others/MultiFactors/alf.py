import numpy as np
import pandas as pd
from Operator import Op


class Alpha(object):
    
    def __init__(self, daynums, stknums):
        self._alpha = np.full([daynums, stknums], np.nan)

    def run(self, hd):
        '''
        Calculate your alpha here.
        '''
        pass
    
    def save(self, name):
        
        np.save(name, self._alpha)
        print("save successfully!")
        
    def get(self):
        return self._alpha
    
    
class Alphatest(Alpha):
    
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 0
        #data = self.close.shift(5)-self.close
        data = hd['close']-hd['open']

        start = hd['startidx']
        end = hd['endidx']
        #start = np.where(data.index == self.start)[0].tolist()[0]
        #end = np.where(data.index == self.end)[0].tolist()[0]
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        #print("Neutralize is finished!")
        
        

class Alpha1(Alpha):
    '''
    shrp 3.33
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        data = -hd['close'].rolling(10).corr(hd['volume'])

        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")

class Alpha1P(Alpha):
    '''
    shrp 0.7147
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        data = -hd['close'].rolling(10).corr(hd['volume'])

        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
        self._alpha = Op.personalize(self._alpha)
        print("Personize is finished!")
    
        
class Alpha2(Alpha):
    '''
    shrp 2.86
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        data = hd['close'].rolling(10).corr(hd['volume'])
        data = -Op.rank_col(data)
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
        
class Alpha3(Alpha):
    '''
    shrp 3.73
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        data = -hd['amount'].rolling(10).std()
        #data = self.Rank(data)
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")


class Alpha3P(Alpha):
    '''
    shrp 0.7828
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        data = -hd['amount'].rolling(10).std()
        #data = self.Rank(data)
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")

        self._alpha = Op.personalize(self._alpha)
        print("Personize is finished!")
        
        
class Alpha4(Alpha):
    '''
    shrp 5.88
    GTJA 1
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        lnvol = np.log(hd['volume'])
        lnvol_d = lnvol-lnvol.shift()
        rank1 = Op.rank_col(lnvol_d)
        rank2 = Op.rank_col((hd['close']-hd['open'])/hd['open'])
        corr = rank1.rolling(6).corr(rank2)
        data = -corr
        #data = self.Rank(data)
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")

class Alpha4P(Alpha):
    '''
    shrp 0.6
    GTJA 1
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        lnvol = np.log(hd['volume'])
        lnvol_d = lnvol-lnvol.shift()
        rank1 = Op.rank_col(lnvol_d)
        rank2 = Op.rank_col((hd['close']-hd['open'])/hd['open'])
        corr = rank1.rolling(6).corr(rank2)
        data = -corr
        #data = self.Rank(data)
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
        self._alpha = Op.personalize(self._alpha)
        print("Personize is finished!")

class Alpha5(Alpha):
    '''
    shrp 2.61
    GTJA 2
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        data1 = ((hd['close']-hd['low'])-(hd['high']-hd['close']))/(hd['high']-hd['low'])
        data = (data1-data1.shift())*-1
        #data = self.Rank(data)
        
        start = hd['startidx']
        end = hd['endidx']

        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
        
class Alpha6(Alpha):
    '''
    shrp 4.58
    GTJA 7
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        data1 = hd['vwap']-hd['close']
        data1[data1<3] = 3
        rank1 = Op.rank_col(data1)
        
        data2 = hd['vwap']-hd['close']
        data2[data2>3] = 3
        rank2 = Op.rank_col(data2)
        volume = hd['volume']
        volume[volume==0] = np.nan
        rank3 = Op.rank_col(volume-volume.shift(3))
        data = rank1+rank2*rank3
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")

class Alpha6P(Alpha):
    '''
    shrp -0.538
    GTJA 7
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        data1 = hd['vwap']-hd['close']
        data1[data1<3] = 3
        rank1 = Op.rank_col(data1)
        
        data2 = hd['vwap']-hd['close']
        data2[data2>3] = 3
        rank2 = Op.rank_col(data2)
        volume = hd['volume']
        volume[volume==0] = np.nan
        rank3 = Op.rank_col(volume-volume.shift(3))
        data = rank1+rank2*rank3
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
        self._alpha = Op.personalize(self._alpha)
        print("Personize is finished!")

class Alpha7(Alpha):
    '''
    shrp 2.38
    GTJA 16
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        rank1 = Op.rank_col(hd['volume'])
        rank2 = Op.rank_col(hd['vwap'])
        corr = rank1.rolling(5).corr(rank2)
        rank3 = Op.rank_col(corr)
        data = -1*rank3.rolling(5).max()
        #for ii in range(window, corr.shape[0]+1):
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
    
class Alpha7P(Alpha):
    '''
    shrp 0.815
    GTJA 16
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        rank1 = Op.rank_col(hd['volume'])
        rank2 = Op.rank_col(hd['vwap'])
        corr = rank1.rolling(5).corr(rank2)
        rank3 = Op.rank_col(corr)
        data = -1*rank3.rolling(5).max()
        #for ii in range(window, corr.shape[0]+1):
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
        self._alpha = Op.personalize(self._alpha)
        print("Personize is finished!")
        
class Alpha8(Alpha):
    '''
    shrp 8.63
    GTJA 114
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1

        data1 = (hd['high']-hd['low'])/(hd['close'].rolling(5).sum()/5)

        #rank1 = self.rank_col(data1)
        rank1 = Op.rank_col(data1.shift(2))
        rank2 = Op.rank_col(hd['volume'])
    
        data3 = data1/(hd['vwap']-hd['close'])
        data3[data3==0] = np.nan
        data = rank1*rank2/data3
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
class Alpha8P(Alpha):
    '''
    shrp 0.231
    GTJA 114
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1

        data1 = (hd['high']-hd['low'])/(hd['close'].rolling(5).sum()/5)

        #rank1 = self.rank_col(data1)
        rank1 = Op.rank_col(data1.shift(2))
        rank2 = Op.rank_col(hd['volume'])
    
        data3 = data1/(hd['vwap']-hd['close'])
        data3[data3==0] = np.nan
        data = rank1*rank2/data3
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
        self._alpha = Op.personalize(self._alpha)
        print("Personize is finished!")
      

class Alpha10(Alpha):
    '''
    shrp 2.684
    GTJA 16
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1

        rank1 = Op.rank_col(hd['volume'])
        rank2 = Op.rank_col(hd['vwap'])
        
        corr = rank1.rolling(5).corr(rank2)
        rank3 = Op.rank_col(corr)
        
        tsmax = rank3.rolling(5).max()
        
        data = -tsmax
        
        start = hd['startidx']
        end = hd['endidx']
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")

class Alpha10P(Alpha):
    '''
    shrp 0.815
    GTJA 16
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1

        rank1 = Op.rank_col(hd['volume'])
        rank2 = Op.rank_col(hd['close'])
        
        corr = rank1.rolling(5).corr(rank2)
        rank3 = Op.rank_col(corr)
        
        tsmax = rank3.rolling(5).max()
        
        data = -tsmax
        
        startdate = hd['startdate']
        enddate = hd['enddate']
        start = hd['startidx']
        end = hd['endidx']
        
        for di in range(start, end+1):
            self._alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
        self._alpha = Op.personalize(self._alpha)
        print("Person is finished!")
        
        self._alpha, self.trend = Op.trend(self._alpha, startdate, enddate)
        print("Trend is finished!")