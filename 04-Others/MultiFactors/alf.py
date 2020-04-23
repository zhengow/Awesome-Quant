import numpy as np
import pandas as pd

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
            #start = np.where(inds.index == start)[0].tolist()[0]
            #end = np.where(inds.index == end)[0].tolist()[0]
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
    
    def rank_col(data):
        return pd.DataFrame(data).rank(pct=True, axis=1)
    def rank_row(data):
        return pd.DataFrame(data).rank(pct=True, axis=0)
    def tsmax(data, window):
        rank = np.full([data.shape[0], data.shape[1]], np.nan)
        for ii in range(window, data.shape[0]+1):
            tmp = data.iloc[ii-window:ii,:]
            rank[ii-1,:] = self.rank_row(tmp).iloc[-1]
        return rank
    

class Alpha(object):
    
    def __init__(self, daynums, stknums):
        self._alpha = np.full([daynums, stknums], np.nan)

    def run(self, hd):
        '''
        Calculate your alpha here.
        '''
        pass
        
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
    shrp 1.724
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        data = hd['close'].rolling(10).corr(hd['vol'])

        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self.alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
        
    
        
class Alpha2(Alpha):
    '''
    shrp 1.9909
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        data = hd['close'].rolling(10).corr(hd['volume'])
        data = Op.rank_col(data)
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self.alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
        


class Alpha3(Alpha):
    '''
    shrp 1.312
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        data = hd['amount'].rolling(10).std()
        #data = self.Rank(data)
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self.alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
        
class Alpha4(Alpha):
    '''
    shrp 1.814
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
            self.alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
        

class Alpha5(Alpha):
    '''
    shrp 2.914
    GTJA 2
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1
        #data = self.close.shift(5)-self.close
        data1 = ((hd['close']-hd['low'])-(hd['high']-hd['close']))/(hd['high']-hd['low'])
        data = data1-data1.shift()
        #data = self.Rank(data)
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self.alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
        
class Alpha6(Alpha):
    '''
    shrp 3.797
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
        
        self.volume[self.volume==0] = np.nan
        rank3 = self.rank_col(self.volume-self.volume.shift(3))
        data = rank1+rank2*rank3
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self.alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")

class Alpha7(Alpha):
    '''
    shrp 3.797
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
        window = 5
        for ii in range(window, corr.shape[0]+1):
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self.alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")

class Alpha8(Alpha):
    '''
    shrp 4.621
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
    
        data3 = data1/(self.vwap-self.close)
        data3[data3==0] = np.nan
        data = rank1*rank2/data3
        
        start = hd['startidx']
        end = hd['endidx']
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        for di in range(start, end+1):
            self.alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        
        

class Alpha9(Alpha):
    '''
    shrp 7.588
    GTJA 119
    '''
    def run(self, hd):
        '''
        Calculate!
        '''
        delay = 1

        self.volume[self.volume==0] = np.nan

        data1 = self.volume.rolling(5).mean()
        data1 = data1.rolling(26).sum()
        corr = self.vwap.rolling(5).corr(data1)
        data1 = corr.ewm(7).mean()
        rank1 = self.rank_col(data1)
        rank1 = np.array(rank1)
        rank2 = self.rank_col(self.open)
        rank3 = self.rank_col(self.volume.rolling(15).mean())
        corr2 = rank2.rolling(21).corr(rank3)
        window = 7
        rank4 = Op.tsrank(corr, 7)
        #rank4 = np.full([corr2.shape[0], corr2.shape[1]], np.nan)
        #for ii in range(window, corr2.shape[0]+1):
        #    tmp = corr2.iloc[ii-window:ii,:]
        #    rank4[ii-1,:] = self.rank_row(tmp).iloc[-1,:]
        
        data2 = pd.DataFrame(rank4)
        data2 = data2.ewm(8).mean()
        rank5 = self.rank_col(data2)
        rank5 = np.array(rank5)
        data = rank5-rank1
        data = pd.DataFrame(data)
        #start = np.where(data.index == self.start)[0].tolist()[0]
        #end = np.where(data.index == self.end)[0].tolist()[0]
        
        #self.alpha = data.iloc[start-delay:end+1,:]
        
        start = hd['startidx']
        end = hd['endidx']
        
        for di in range(start, end+1):
            self.alpha[di-start,:] = data.iloc[di-delay,:]
        print("Alpha is finished!")
        
        self._alpha = Op.Neutralize('IND', self._alpha, start, end)
        print("Neutralize is finished!")
        

        
        
