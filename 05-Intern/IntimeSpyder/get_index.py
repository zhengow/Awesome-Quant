from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import COOKIES
from urllib.parse import quote
import datetime
import time
import queue
import math
import pandas as pd
import numpy as np
import threading
import sys                                                                  
import signal

def quit(signum, frame):
    print()
    print('stop fusion')
    sys.exit()

class BaiduIndex:
    """
        股票baidu搜索指数
        :keywords; list
    """
    '''
    _cookies = [{'name': cookie.split('=')[0],
            'value': cookie.split('=')[1]}
           for cookie in COOKIES.replace(' ', '').split(';')]
    '''

    
    _all_kind = ['all', 'pc', 'wise']
    _params_queue = queue.Queue()
    def __init__(self, keywords: list):
        self.keywords = keywords
        self._init_queue(keywords)
        self.index = self._init_df(keywords)
        self.count = 0
        self.duration = time.time()

    def _init_queue(self, keywords):
        """
            初始化参数队列
        """
        keywords_list = self._split_keywords(keywords)
        for keywords in keywords_list:
            self._params_queue.put(keywords)
    
    def _init_df(self, keywords):
        """
            初始化最终结果
        """
        index_time = np.full([24],'2000-01-01 00:00:00')
        index_time[0] = self.open_browser()
        for i in range(23):
            tmp = datetime.datetime.strptime(index_time[i], '%Y-%m-%d %H:%M:%S')+datetime.timedelta(hours=1)
            index_time[i+1] = datetime.datetime.strftime(tmp, "%Y-%m-%d %H:%M:%S")
        initial = {'time': index_time}
        for item in keywords:
            tmp = np.full([24],np.nan)
            initial[item] = tmp
        
        df = pd.DataFrame(initial)
        df = df.set_index(['time'])
        print("init_df is finished!!")
        return df
                
    
    def _split_keywords(self, keywords: list) -> [list]:
        """
        对关键词进行切分
        """
        return [keywords[i*5: (i+1)*5] for i in range(math.ceil(len(keywords)/5))]
    
    def open_browser(self, which = 20):
        
        cookies = [{'name': cookie.split('=')[0],
                    'value': cookie.split('=')[1]}
                   for cookie in COOKIES[which].replace(' ', '').split(';')]

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get('https://index.baidu.com/#/')
        browser.set_window_size(1500, 900)
        browser.delete_all_cookies()
        for cookie in cookies:
            browser.add_cookie(cookie)
        stk = '000001'
        url = 'https://index.baidu.com/v2/main/index.html#/trend/%s?words=%s' % (stk,quote(stk))
        browser.get(url)
        time.sleep(1)
        browser.find_elements_by_xpath('//*[@class="veui-button"]')[1].click()
        browser.find_elements_by_xpath('//*[@class="list-item"]')[0].click()
        time.sleep(1)
        if(which == 20):
            starttime = self.move(browser, '', which)
            browser.quit()
            return starttime
        
        return browser
    
    
    def move(self, browser, keyword, which = 0):
        #there will be some problems
        try:
            base_node = browser.find_elements_by_xpath('//*[@class="index-trend-chart"]')[0]
        except Exception as e:
            print("The message is from here!!!")
        #print(base_node)
        chart_size = base_node.size
        move_step = 24 - 1
        step_px = chart_size['width'] / move_step
        cur_offset = {
            'x': step_px,
            'y': chart_size['height'] - 50
        }

        webdriver.ActionChains(browser).move_to_element_with_offset(
            base_node, 1, cur_offset['y']).perform()
    
        date = base_node.find_element_by_xpath('./div[2]/div[1]').text

        
        if(which != 0):
            print(date)
            return date
        
        index = base_node.find_element_by_xpath('./div[2]/div[2]/div[2]').text
        
        index = index.replace(',', '')
        index = index.replace(' ', '')
        if(index!=''):
            self.index.loc[date,keyword] = int(index)
        
    
        for _ in range(24-1):
            #time.sleep(0.05)
            webdriver.ActionChains(browser).move_to_element_with_offset(
                base_node, int(cur_offset['x']), cur_offset['y']).perform()
            cur_offset['x'] += step_px
            date = base_node.find_element_by_xpath('./div[2]/div[1]').text
            index = base_node.find_element_by_xpath('./div[2]/div[2]/div[2]').text
            index = index.replace(',', '')
            index = index.replace(' ', '')
            if(index!=''):
                self.index.loc[date,keyword] = int(index)
        if(self.count%100 == 0 and self.count != 0):
            print("100 stocks use ",time.time()-self.duration,"s")
            self.duration = time.time()
        else:
            print(keyword,': ',self.count," stocks is finished")
        self.count = self.count + 1
        
    
    def visit(self, browser, stks):
        for keyword in stks:
            url = 'https://index.baidu.com/v2/main/index.html#/trend/%s?words=%s' % (keyword,quote(keyword))
            browser.get(url)
            time.sleep(0.5)
            if(browser.find_elements_by_xpath('//*[@class="not-in"]')):
                continue
            else:
                self.move(browser, keyword)
            
            
    def doTask(self, i):
        browser = self.open_browser(i)
        #signal.signal(signal.SIGINT, quit)
        #signal.signal(signal.SIGTERM, quit)
        error = 0
        while 1:
            try:
                params_data = self._params_queue.get(timeout=1)
                self.visit(browser, params_data)

            except queue.Empty:
                break
            except Exception as e:
                error = error + 1
                print(e)
                self._params_queue.put(params_data)
                if(error > 50):
                    break
        browser.quit()
        print("thread ", i, "is finished!!!")
            
        
    
    def run(self, numThread = 5):
        """
        open multi thread to run tasks:
            first it open browser, then 
            each tasks will do for loop to get keywords and save the res to self._index
        """
        threads = []
        for i in range(numThread):
            thread = threading.Thread(target=self.doTask, args=(i,))
            threads.append(thread)
            thread.start()
            
        for th in threads:
            th.join()
        print("all the threads are finished!")
        
    
    def get_index(self):
        return self.index
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    