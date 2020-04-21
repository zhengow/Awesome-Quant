import pandas as pd
import numpy as np

class Data():
    
    def __init__():
        pass
        #self.trade_date = self.get_trade_date(start_date, end_date)
        
    '''
    def get_trade_date(start_date, end_date):
        
        date = pd.read_csv('date.csv')
        return date.loc[start_date:end_date,:]
    '''
    
    def get(data, startdate, enddate, hist = 0):

        if(data=='date'):
            start = 0
            end = 0
            df = pd.read_csv('date.csv')
            for ii in range(df.shape[0]):
                if(df['date'][ii]>startdate):
                    start = ii
                    break
            for ii in range(start+1, df.shape[0]):
                if(df['date'][ii]>enddate):
                    end = ii
                    break
            return df['date'][start:end]
        
        try:
            df = pd.read_csv(data+'.csv', index_col='date')
            start = np.where(df.index == startdate)[0].tolist()[0]-hist
            end = np.where(df.index == enddate)[0].tolist()[0]
            return df.iloc[start:end+1,:]
        except Exception as e:
            print(e)
