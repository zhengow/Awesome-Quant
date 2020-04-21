from alf import *
from backtest import BacktestEngine

if __name__ == '__main__':
    
    start = '2010-01-01'
    end = '2020-01-01'
    alpha = Alpha1(start,end)
    bte = BacktestEngine(alpha)
    #bte.prints()
    #bte.show()