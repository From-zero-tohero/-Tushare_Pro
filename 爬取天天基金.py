# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 20:38:12 2021

@author: 曹进辉
"""

import requests
import time
import execjs
import pandas as pd
import tushare as ts
import talib

from pyecharts import options as opts
from pyecharts.charts import Line, Grid
import os

# 使用 Tushare API 下载文件时所需要用到的 tocken



"""初始化 Tushare API 的参数"""
ts.set_token(Tushare_Tocken)
pro = ts.pro_api()

# 获取今天的日期
today = time.strftime('%Y%m%d',time.localtime(time.time()))

# 获取交易日信息
df_date = pro.query('trade_cal', end_date=today)
# is_open = 1 代表这一天股票开市
df_date = df_date[df_date['is_open'] == 1]

# 按照时间进行倒序排列，因为爬取到的基金数据是按照倒顺序排列
df_date = df_date.sort_values(by=['cal_date'],ascending=False)

fund_code = {'160106', '160221', '002907', '001856', '011103', '001553','004854', '161726', '163406', '162605', '006308', '519196',
             '004224', '162703', '001009', '003834', '000751', '003095', '009225', '005827', '002692', '320007', '008087', '010253',
             '001500', '001475', '001838', '167301', '161620', '160639', '164403', '161725', '001156'}


# 接口构造

# 构造一个url
def getUrl(fscode):
    head = 'http://fund.eastmoney.com/pingzhongdata/'
    tail = '.js?v='+ time.strftime("%Y%m%d%H%M%S",time.localtime())
    return head+fscode+tail


# 获取净值
def getWorth(fscode):
    #用requests获取到对应的文件
    URL= getUrl(fscode)

    content = requests.get(URL).text
    #使用execjs获取到相应的数据

    jsContent = execjs.compile(content)
    name = jsContent.eval('fS_name')
    code = jsContent.eval('fS_code')
    #单位净值走势
    netWorthTrend = jsContent.eval('Data_netWorthTrend')
    #累计净值走势
    ACWorthTrend = jsContent.eval('Data_ACWorthTrend')
    netWorth = []
    ACWorth = []
   #提取出里面的净值
    for dayWorth in netWorthTrend[::-1]:
        netWorth.append(dayWorth['y'])
    for dayACWorth in ACWorthTrend[::-1]:
        ACWorth.append(dayACWorth[1])
    print(name,code)
    
    return netWorth, ACWorth, name


code_name = {}
fund_data = pd.DataFrame()
for code in fund_code:
    netWorth, ACWorth, name = getWorth(code)
    code_date = df_date.iloc[:len(netWorth)]
    code_name[code] = name
    new_data = pd.DataFrame()
    new_data['date'] = code_date['cal_date'].values
    new_data['netWorth'] = netWorth
    
    new_data = new_data.sort_values(by=['date'])
    new_data["date"] = pd.to_datetime(new_data["date"])
    new_data["date"] = new_data.date.apply(lambda x: x.strftime("%Y-%m-%d"))
    
    new_data['MACD'], new_data['MACDsignal'], new_data['MACD hist'] = talib.MACD(new_data['netWorth'], 
                                                                                 fastperiod=12, slowperiod=26, signalperiod=9)

    new_data['code'] = code
    new_data['name'] = name
    fund_data = fund_data.append(new_data)
#    time.sleep(1)

for code in fund_code:
    new_data = fund_data[fund_data['code'] == code]
    if new_data.iloc[-1,]['MACD'] > new_data.iloc[-1,]['MACDsignal'] and new_data.iloc[-2,]['MACD'] <= new_data.iloc[-2,]['MACDsignal']:
        print('刚刚穿过')
        print("买入基金：{}".format(code_name[code]))
        print(code)
        continue
    if new_data.iloc[-1,]['MACD'] < new_data.iloc[-1,]['MACDsignal'] and new_data.iloc[-2,]['MACD'] >= new_data.iloc[-2,]['MACDsignal']:
        print("卖出基金：{}".format(code_name[code]))
        print(code)
        continue
    if new_data.iloc[-1,]['MACD'] > new_data.iloc[-1,]['MACDsignal']:
        print("买入基金：{}".format(code_name[code]))
        print(code)
        continue
    if new_data.iloc[-1,]['MACD'] < new_data.iloc[-1,]['MACDsignal']:
        print("卖出基金：{}".format(code_name[code]))
        print(code)


fund_data.to_csv('data/fund_data.csv', index =False)