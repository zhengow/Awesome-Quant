from ML import Mlalpha
from backtest import BacktestEngine
from data import Data
import numpy as np
import pandas as pd

if __name__ == '__main__':
    
    start = '2010-01-01'
    end = '2020-01-01'
    trade_date = Data.get('date', start, end)
    #close = Data.get('close', start_trade, end_trade, hist)
    
    alpha1 = np.load('alpha1.npy')
    alpha4 = np.load('alpha4.npy')
    alphas = [alpha1, alpha4]
    
    #which alpha
    mlalpha = Mlalpha(alphas, trade_date)
    mlalpha.set_model()
    mlalpha.train()
    mlalpha.predict()
    alpha = mlalpha._alphas['test']
    
    bte = BacktestEngine(alpha, trade_date)
    bte.prints()
    bte.show()
