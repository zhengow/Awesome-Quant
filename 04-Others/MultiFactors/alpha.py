import numpy as np
import pandas as pd

class Alpha():
    
    def __init__(self, start_date, end_date, hist = 10):
        self.hist = hist
        self.trade_date = self.get_trade_date(start_date, end_date)
        self._init_data()
    
    def _init_data(self):
        pass
        
    def run(self):
        '''
        Calculate your alpha here.
        '''
        pass
    
    def get_alpha(self):
        return self.alpha
        
    def Neutralize(self, method):
        if(method == "IND"):
            1
        if(method == "MV"):
            1
        else:
            print("No such Neutralization!!")
    
    def Rank(self):
        return pd.DataFrame(self.alpha).rank(pct=True, axis=1)

class Alpha1(Alpha):
    
    def run(self):
        '''
        Calculate!
        '''
    def _init_data(self, hist):
        data = Data()
        hist = 10
        self.close = data.get('close', hist)
        self.high = data.get('high', hist)
        self.alpha = np.full([])
        