import tushare as ts
import pandas as pd
import numpy as np
import time
from Operator import Op
import smtplib
from email.mime.text import MIMEText

def run():
    pro = ts.pro_api()
    today = time.strftime('%Y.%m.%d',time.localtime(time.time()))
    today = today.replace('.','') #consider +1
    lastMonth = time.strftime('%Y.%m.%d',time.localtime(time.time()-2592000))
    lastMonth = lastMonth.replace('.','')
    
    close = pd.DataFrame()
    volume = pd.DataFrame()
    
    stkdata = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code, name, industry')
    i = 1
    for code in stkdata['ts_code'][:100]:
        print(i)
        i = i + 1
        try:
            df = ts.pro_bar(ts_code=code, adj='hfq', start_date=lastMonth, end_date=today)
            close[code] = df['close'].iloc[::-1]
            volume[code] = (df['amount']/df['close']*10).iloc[::-1]
        except Exception as e:
            print(e)
    
    # close = oclose.copy()
    # volume = ovolume.copy()
    
    cols = np.where(pd.isnull(close)|pd.isnull(volume))[1]
    colnames = close.columns[cols].unique()
    for name in colnames:
        del close[name]
        del volume[name]
    
    rank1 = Op.rank_col(volume)
    rank2 = Op.rank_col(close)
    
    corr = rank1.rolling(5).corr(rank2)
    rank3 = Op.rank_col(corr)
    
    tsmax = rank3.rolling(5).max()
    
    data = -tsmax
    
    #alpha = np.full([1, close.shape[1]], np.nan)
    alpha = data.iloc[-1,:]
    print("Alpha is finished!")
    
    alpha = Neutralize(alpha, stkdata)
    #print("Neutralize is finished!")
    alpha[pd.isnull(alpha)] = -10
    idx = np.argpartition(alpha, -5)[-5:]
    
    stks = alpha[idx]
    
    inx = pro.index_daily(ts_code='000905.SH', start_date=lastMonth, end_date=today)['close']
    
    trend = (inx.rolling(5).mean()-1.01*inx.rolling(10).mean()).iloc[-1]
    
    content = 'trend: '+str(trend)+'\n'
    for ii in range(stks.shape[0]):
        content = content+str(stks.index[ii])+':'+str(stks.iloc[ii])+'\n'
    
    send(content)
    
    return

def Neutralize(alphas, data):
    data.set_index(data['ts_code'], inplace=True)
    inds = data['industry'].unique()
    for ind in inds:
        idx = []
        for ii in range(alphas.shape[0]):
            if(ind == data.loc[alphas.index[ii]]['industry']):
                idx.append(ii)
        mean = np.nanmean(alphas[idx])
        for ii in idx:
            alphas[ii] = alphas[ii] - mean
    return alphas

def send(content):
    msg_from='313407040@qq.com'                                 #发送方邮箱
    passwd='kgxvnbvdetuabgeb'                                   #填入发送方邮箱的授权码
    msg_to='zhengow@qq.com'                                  #收件人邮箱
                                
    subject="This Week Stocks"                                     #主题        
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com",465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print('success')
    except Exception as e:
        print(e)
        print('fail')
    finally:
        s.quit()


if __name__ == '__main__':
    
    while True:
            
        run()
        
        
        
        