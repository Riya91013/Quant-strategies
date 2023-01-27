# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 21:09:18 2023

@author: riyas
"""

import pandas as pd
import pandas_ta as ta

df = pd.read_csv(r"C:\Users\riyas\Downloads\nifty1hr.csv")


df.drop(['open', 'high', 'low'], axis = 1, inplace = True)
df.set_index(df.datetime, inplace = True)
df.drop(['datetime'], axis = 1, inplace = True)

status = 0
entry_price = 0
entry_datetime = 0
exit_price = 0
exit_datetime = 0

tre = ta.rsi(df.close, length = 14)

rsi_res = pd.concat([df,tre], axis = 1, join = 'inner')
#rsi_res.drop(['index'], axis = 1, inplace = True)

pnl = pd.DataFrame(columns = ['Entry date time', 'Entry price', 'Exit date time', 'Exit price'])

cnt = 0
ok = False

for row, value in rsi_res.iterrows():
    if(value[1] > 40 and value[1] < 60) and status == 0:
        ok = True
        status = 1
        entry_price = value[0]
        entry_datetime = row
    
    if(ok):
        cnt+=1
        
    if(cnt == 10) or ((value[1] > 80) and status == 1):
        ok = False
        cnt = 0
        status = 0
        exit_price = value[0]
        exit_datetime = row
        
        
    if(exit_price >0) and status == 0:
        list_res = []
        list_res.append(entry_datetime)
        list_res.append(entry_price)
        list_res.append(exit_datetime)
        list_res.append(exit_price)
        pnl.loc[len(pnl)] = list_res
        entry_price = 0
        exit_price = 0
    
pnl['profit'] = pnl['Exit price'] - pnl['Entry price']

pnl.to_csv(r"C:\Users\riyas\Downloads\pnl_rsi_new_imp_2l.csv")
    
        