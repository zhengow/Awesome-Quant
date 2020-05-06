import numpy as np
import pandas as pd
from Operator import Op
from data import Data

class Mlalpha(object):
    
    def __init__(self, alphas, trade_date):
        
        dailyret = Data.get('ret2', trade_date.iloc[0], trade_date.iloc[-1])
        self.start = np.where(dailyret.index == trade_date.iloc[0])[0].tolist()[0]
        self.end = np.where(dailyret.index == trade_date.iloc[-1])[0].tolist()[0]
        
        stop = Data.get('all', trade_date.iloc[0], trade_date.iloc[-1])
        dailyret[pd.isnull(stop)] = np.nan
        dailyret = np.array(dailyret)
        
        self.num = len(alphas)
        self.row = alphas[0].shape[0]
        self.col = alphas[0].shape[1]
        self._alpha = np.full([self.row, self.col], np.nan)
        self._y = dailyret.reshape(-1,1)
        self._trainalpha = np.full([self.num, self.row, self.col], np.nan)
        self._x = np.full([self.row*self.col, self.num], np.nan)
        self.resize(alphas)
        #self._models = self.set_model()
        #self._init_alpha()
        #self._alphas = np.full([alphas[0].shape[0], alphas[0].shape[1]], np.nan)
        
    
    def set_model(self, models):
        '''
        add the model we want to use here
        '''
        self._models = models
        
        #models = {'test':svm.SVR()}
        
        #return models
    
    def resize(self, alphas):
        '''
        version 1
        '''

        for ii, alpha in enumerate(alphas):
            self._trainalpha[ii,:,:] = alpha
        
        row = -1
        for ii in range(self._trainalpha.shape[1]):
            for jj in range(self._trainalpha.shape[2]):
                row = row + 1
                self._x[row, :] = self._trainalpha[:,ii,jj]
    
    def get(self):
        return self._alphas
    
    def train(self, window = 1):
        window = self.col*window
        x = self._x[:window,:]
        y = self._y[:window,:]
        
        xnanrow = np.where(pd.isnull(x))[0]
        ynanrow = np.where(pd.isnull(y))[0]
        deleterow = np.unique(np.append(ynanrow, xnanrow))
        x = np.delete(x, deleterow, axis = 0)
        y = np.delete(y, deleterow, axis = 0)

        for key,model in self._models.items():
            model.fit(x,y)
    
    def predict(self):
        nums = self.col #each time feed how much data
        
        for key, model in self._models.items():
            for ii in range(self.row):
                x = self._x[ii*nums:(ii+1)*nums,:]
                xnanrow = np.where(pd.isnull(x))[0]
                nanrow = np.unique(xnanrow)
                x[pd.isnull(x)] = 0
                y = model.predict(x)
                y[nanrow] = np.nan
                self._alpha[ii,:] = y.reshape(1,-1)
        
        self._alpha = Op.Neutralize('IND', self._alpha, self.start, self.end)
        print("Neutralize is finished!")
        
        
        
        