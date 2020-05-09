from alf import Alpha8
from backtest import BacktestEngine
from data import Data
import numpy as np
import pandas as pd

if __name__ == '__main__':
    
    start = '2010-01-01'
    end = '2020-04-01'
    trade_date = Data.get('date', start, end)
    tradedays = trade_date.shape[0]
    start_trade = trade_date.iloc[0]
    end_trade = trade_date.iloc[-1]
    hist = 50
    ops = Data.get('open', start_trade, end_trade, hist)
    high = Data.get('high', start_trade, end_trade, hist)
    low = Data.get('low', start_trade, end_trade, hist)
    vwap = Data.get('vwap', start_trade, end_trade, hist)
    close = Data.get('close', start_trade, end_trade, hist)
    volume = Data.get('volume', start_trade, end_trade, hist)
    amount = Data.get('amount', start_trade, end_trade, hist)
    volume[volume==0] = np.nan
    stknums = close.shape[1]
    startidx = np.where(close.index == start_trade)[0].tolist()[0]
    endidx = np.where(close.index == end_trade)[0].tolist()[0]
    hd = {'amount':amount, 'close':close, 'open':ops, 'high':high, 'low':low, 'vwap':vwap, 'volume':volume, 'startidx':startidx, 'endidx':endidx, 'stknums':stknums}

    #which alpha
#    alpha = Alpha8(tradedays, stknums)
#    alpha.run(hd)
#    alpha.save('alpha8_1')
    name = "alpha8_1"
    alpha = np.load(name+'.npy')
    bte = BacktestEngine(alpha, trade_date, name)
    bte.prints()
    bte.show()
