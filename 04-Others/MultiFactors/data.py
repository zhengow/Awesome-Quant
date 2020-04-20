import pandas as pd

class Data():
    
    def __init__(self, start_date, end_date):
        
        self.trade_date = self.get_trade_date(start_date, end_date)
        
    
    def get_trade_date(self, start_date, end_date):
        date = pd.read_csv('date.csv')
        return date.loc[start_date:end_date,:]
    
    def get(self, data, hist = 0):
        if(data=='close'):
            load_data = pd.DataFrame('close.csv')
        if(data=='high'):
            1
        if(data=='low'):
            1
        if(data=='open'):
            1
        if(data=='vwap'):
            1
        if(data=='high'):
            1
        if(data=='close'):
            1
        if(data=='high'):
            1
        
        if(self.trade_date.index[0]-hist<0):
            print("Out of time range!")
            return
        
        return load_data.iloc[self.trade_date.index[0]-hist:self.trade_date.index[-1],:]