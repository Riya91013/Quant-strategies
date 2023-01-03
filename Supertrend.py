# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 23:42:09 2022

@author: riyas
"""

#importing modules
import pandas as pd
import pandas_ta as ta

#reading the csv file
df = pd.read_csv(r"C:\Users\riyas\Downloads\BNF_FUT.csv")
df.drop(columns = ['Symbol','Expiry', 'Volume', 'OI'], axis = 1, inplace = True)
#df.set_index(pd.DatetimeIndex(df.Time), inplace = True)
#df.drop(columns = ['Time', 'Date'], axis = 1, inplace = True)

agg = {"Open":"first", "High":"max", "Low":"min", "Close":"last"}

#thirty = df
Date = []
Time = []
Open = []
High = []
Low = []
Close = []
j = 30

for i in range(0,379218,j):
    Date.append(df['Date'][i])
    Time.append(df['Time'][i])
    Open.append(df['Open'][i])
    Close.append(df['Close'][i])
    High.append(max(df['High'][i:i+j]))
    Low.append(min(df['Low'][i:i+j]))

#print(df['Date'][0])

temp = pd.DataFrame({'Date': Date, 'Time':Time, 'Open':Open, 'High':High, 'Low':Low, 'Close':Close})

temp['Datetime'] = temp['Date'] +" "+ temp['Time']
temp.set_index(temp.Datetime, inplace = True)
temp.drop(columns = ['Date', 'Time', 'Datetime'], axis = 1, inplace = True)
#temp

#temp = df.resample(f'{30}min', origin= 'start').agg(agg).dropna()

s1 = ta.supertrend(temp.High, temp.Low, temp.Close, length = 10, multiplier = 3)
s2 = ta.supertrend(temp.High, temp.Low, temp.Close, length = 9, multiplier = 2)
s3 = ta.supertrend(temp.High, temp.Low, temp.Close, length = 8, multiplier = 1)
temp.drop(columns = ['Open', 'High', 'Low'], axis = 1, inplace = True)
s1.drop(columns= ['SUPERT_10_3.0', 'SUPERTl_10_3.0', 'SUPERTs_10_3.0'], axis = 1, inplace = True)
s2.drop(columns= ['SUPERT_9_2.0', 'SUPERTl_9_2.0', 'SUPERTs_9_2.0'], axis = 1, inplace = True)
s3.drop(columns= ['SUPERT_8_1.0', 'SUPERTl_8_1.0', 'SUPERTs_8_1.0'], axis = 1, inplace = True)

suprr_final = pd.concat([temp,s1,s2,s3], axis = 1, join = 'inner')
suprr_final

#0 for no trade
status = 0 
entry_price = 0
entry_datetime = 0
exit_price = 0
exit_datetime = 0
type_trade = ''

pnl = pd.DataFrame(columns = ['Type', 'Entry Date and Time', 'Entry Price', 'Exit Date Time', 'Exit Price'])

for row, value in suprr_final.iterrows():
    
    if status == 0 and value[1] == value[2] == value[3] == 1:
        status = 1
        entry_price = value[0]
        entry_datetime = row
        type_trade = 'Long'
    
    if status == 1 and (value[1] != 1 or value[2] != 1 or value[3] != 1):
        status = 0
        exit_price = value[0]
        exit_datetime = row
        
    if status == 0 and value[1] == value[2] == value[3] == -1:
        status = -1
        entry_price = value[0]
        entry_datetime = row
        type_trade = 'Short'
        
    if status == -1 and (value[1] != -1 or value[2] != -1 or value[3] != -1):
        status = 0
        exit_price = value[0]
        exit_datetime = row
    
    if exit_price > 0 and status == 0:
        list_res = []
        list_res.append(type_trade)
        list_res.append(entry_datetime)
        list_res.append(entry_price)
        list_res.append(exit_datetime)
        list_res.append(exit_price)
        pnl.loc[len(pnl)] = list_res
        entry_price = 0
        exit_price = 0
        
pnl.to_csv(r"C:\Users\riyas\Downloads\pnl_supertrend_final.csv")
