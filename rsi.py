# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 12:39:31 2022

@author: riyas
"""
""" 
buy: RSI >60
Exit: if RSI >80 or RSI <40
 """
import pandas as pd
import pandas_ta as ta

#reading the csv file
df = pd.read_csv(r"C:\Users\riyas\Downloads\BNF_FUT_new.csv")
df.drop(columns = ['Symbol','Expiry', 'Volume', 'OI'], axis = 1, inplace = True)

Date = []
Time = []
Open = []
High = []
Low = []
Close = []
j = 375*14

for i in range(0,379218,j):
    Date.append(df['Date'][i])
    Time.append(df['Time'][i])
    Open.append(df['Open'][i])
    Close.append(df['Close'][i])
    High.append(max(df['High'][i:i+j]))
    Low.append(min(df['Low'][i:i+j]))

temp = pd.concat([df], axis = 1, join = 'inner')
#temp = pd.DataFrame({'Date': Date, 'Time':Time, 'Open':Open, 'High':High, 'Low':Low, 'Close':Close})

temp['Datetime'] = temp['Date'] +" "+ temp['Time']
temp.set_index(temp.Datetime, inplace = True)
temp.drop(columns = ['Date', 'Time', 'Datetime'], axis = 1, inplace = True)
temp

tsr = ta.rsi(temp.Close,length = 14)
#tsr

temp.drop(columns = ['Open', 'High', 'Low'], axis = 1, inplace = True)

rsi_res = pd.concat([temp,tsr], axis = 1, join = 'inner')

#rsi_res

#0 for no trade
status = 0 
entry_price = 0
entry_datetime = 0
exit_price = 0
exit_datetime = 0

pnl = pd.DataFrame(columns = ['Entry Date and Time', 'Entry Price', 'Exit Date Time', 'Exit Price'])


for row, value in rsi_res.iterrows():
    if (value[1] >60 and value[1] < 80) and status == 0:
        status = 1
        entry_price = value[0]
        entry_datetime = row
    
    if(value[1] < 40 or value[1] > 80) and status == 1:
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
        
pnl.to_csv(r"C:\Users\riyas\Downloads\pnl_rsi_final.csv")
        