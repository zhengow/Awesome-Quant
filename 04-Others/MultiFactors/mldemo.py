from ML import Mlalpha
from backtest import BacktestEngine
from data import Data
import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn import tree
from sklearn import svm
from sklearn import neighbors
from sklearn import ensemble
from sklearn.tree import ExtraTreeRegressor


if __name__ == '__main__':
    
    start = '2010-01-01'
    end = '2020-01-01'
    trade_date = Data.get('date', start, end)
    #close = Data.get('close', start_trade, end_trade, hist)
    
    alpha1 = np.load('alpha1.npy')
    alpha2 = np.load('alpha2.npy')
    alpha3 = np.load('alpha3.npy')
    alpha4 = np.load('alpha4.npy')
    alpha5 = np.load('alpha5.npy')
    alpha6 = np.load('alpha6.npy')
    alpha7 = np.load('alpha7.npy')
    alpha8 = np.load('alpha8.npy')
    alphas = [alpha1, alpha2, alpha3, alpha4, alpha5, alpha6, alpha7, alpha8]
    
    #which alpha
    window = 250
    print("window:",window)
    mlalpha = Mlalpha(alphas, trade_date)
    #LASSO
    #RIDGE
    #ensemble.GradientBoostingRegressor(n_estimators=10)
    models = {'test':ensemble.GradientBoostingRegressor(n_estimators=10)}
    mlalpha.set_model(models)
    mlalpha.train(window)
    mlalpha.predict()
    alpha = mlalpha._alpha
    bte = BacktestEngine(alpha, trade_date)
    bte.prints()
    bte.show()
