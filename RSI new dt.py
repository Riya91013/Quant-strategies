# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 09:20:33 2023

@author: riyas
"""
""" 
buy: RSI >60
Exit: if RSI >80 or RSI <40
 """
import pandas as pd
import pandas_ta as ta

#reading the csv file
df = pd.read_csv(r"C:\Users\riyas\Downloads\bank_nifty_new.csv")
#df.drop(columns = ['Symbol','Expiry', 'Volume', 'OI'], axis = 1, inplace = True)

temp = pd.concat([df], axis = 1, join = 'inner')
#temp = pd.DataFrame({'Date': Date, 'Time':Time, 'Open':Open, 'High':High, 'Low':Low, 'Close':Close})

temp.set_index(temp.datetime, inplace = True)
temp.drop(columns = ['datetime', 'open', 'low', 'high', 'symbol', 'volume'], axis = 1, inplace = True)
#temp

tsr = ta.rsi(temp.close,length = 14)
#tsr

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
    if (value[1] >40 and value[1] < 80) and status == 0:
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

pnl['Profit'] = pnl['Exit Price'] - pnl['Entry Price']
#sum = 0

#for i in range(0,7264):
#    sum += pnl['Profit'][i]

#pnl['Net Pnl'] = sum
pnl.to_csv(r"C:\Users\riyas\Downloads\pnl_rsi_new_final.csv")

        

