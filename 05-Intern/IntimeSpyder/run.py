import pandas as pd
from key_word import *
import datetime
import time
from get_index import BaiduIndex

if __name__ == "__main__":
    start = time.time()
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    keywords = getkeywords('stockname.csv')
    keywords = keywords[:500]

    
    index = BaiduIndex(keywords)
    index.run(10) #the parameter is how many thread we want
    res = index.get_index()
    res.to_csv(today+'-index.csv')
    print(time.time()-start)
    
    
    