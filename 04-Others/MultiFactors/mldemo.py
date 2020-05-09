from ML import Mlalpha
from backtest import BacktestML
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
from sklearn import preprocessing
import xgboost as xgb


if __name__ == '__main__':
    
    start = '2010-01-01'
    end = '2020-04-01'
    trade_date = Data.get('date', start, end)
    
    alpha1 = np.load('alpha1_1.npy')
    alpha1 = preprocessing.scale(alpha1,axis=1)
    alpha2 = np.load('alpha2_1.npy')
    alpha2 = preprocessing.scale(alpha2,axis=1)
    alpha3 = np.load('alpha3_1.npy')
    alpha3 = preprocessing.scale(alpha3,axis=1)
    alpha4 = np.load('alpha4_1.npy')
    alpha4 = preprocessing.scale(alpha4,axis=1)
    alpha5 = np.load('alpha5_1.npy')
    alpha5 = preprocessing.scale(alpha5,axis=1)
    alpha6 = np.load('alpha6_1.npy')
    alpha6 = preprocessing.scale(alpha6,axis=1)
    alpha7 = np.load('alpha7_1.npy')
    alpha7 = preprocessing.scale(alpha7,axis=1)
    alphas = [alpha1, alpha2, alpha3, alpha4, alpha5, alpha6, alpha7]
    
    #which alpha
    window = 250
    print("window:",window)
    mlalpha = Mlalpha(alphas, trade_date)
    

#    name = "LASSO:lambda=0.00001"
#    models = {name:Lasso(alpha=0.00001)}
#    name = "XGBOOST"
#    models = {name:xgb.XGBRegressor()}
    name = "GBR"
    models = {name:ensemble.GradientBoostingRegressor(n_estimators=10)}
    mlalpha.set_model(models)
    mlalpha.train(window)
    mlalpha.predict()
    alpha = mlalpha._alpha
    bte = BacktestML(alpha, trade_date, name)
    bte.prints()
    bte.show()
#    n_estimator = []
#    ISS = []
#    OSR = []
#    OSS = []
#    for i in range(10,50,5):
#        n_estimator.append(i)
#        name = "GBR"+str(i)
#        print(name)
#        models = {name:ensemble.GradientBoostingRegressor(n_estimators=i)}
#
#        mlalpha.set_model(models)
#        mlalpha.train(window)
#        mlalpha.predict()
#        alpha = mlalpha._alpha
#        bte = BacktestML(alpha, trade_date, name)
#        bte.prints2()
#        ISS.append(bte.shrp[0])
#        OSS.append(np.nanmean(bte.ret[window:])/np.nanstd(bte.ret[window:])*np.sqrt(252))
#        OSR.append(100*np.nanmean(bte.ret[window:])*252)
#    data = {'n_estimator':n_estimator,'IS_shrp':ISS,'OS_shrp':OSS,'OS_ret':OSR}
#    data = pd.DataFrame(data)
