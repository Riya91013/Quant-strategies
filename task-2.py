# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 10:39:13 2023

@author: riyas
"""
#Resampling data first to day wise and then to month to calculate the count for each month if the mob=vement was either 10% up or down from the opening of the month
#and then moving onto the next month
import pandas as pd

df = pd.read_csv(r"C:\Users\riyas\Downloads\RELIANCE.csv")
df.set_index(df.datetime, inplace = True)
#df.drop(columns = ['datetime'], axis = 1, inplace = True)
df.index = pd.to_datetime(df.index)

opening=df.resample('D',origin= 'start').first()
opening.drop(['high','low','close','volume','symbol'],axis=1,inplace=True)

high=df.resample('D',origin= 'start').max()
high.drop(['open','low','close','volume','symbol','datetime'],axis=1,inplace=True)

low=df.resample('D',origin= 'start').min()
low.drop(['open','high','close','volume','symbol','datetime'],axis=1,inplace=True)

close=df.resample('D',origin= 'start').last()
close.drop(['open','low','high','volume','symbol','datetime'],axis=1,inplace=True)

DF=pd.concat([opening,high,low,close],axis=1)
DF.rename(columns = {'datetime':'Datetime'}, inplace = True)
DF.dropna(inplace=True)
#DF.set_index(DF.datetime, inplace = True)

opening_month = df.resample('M',origin= 'start').first()
opening_month.drop(['high','low','close','volume','symbol'],axis=1,inplace=True)

high_month = df.resample('M',origin= 'start').max()
high_month.drop(['open','low','close','volume','symbol','datetime'],axis=1,inplace=True)

low_month = df.resample('M',origin= 'start').min()
low_month.drop(['open','high','close','volume','symbol','datetime'],axis=1,inplace=True)

close_month = df.resample('M',origin= 'start').last()
close_month.drop(['open','low','high','volume','symbol','datetime'],axis=1,inplace=True)

new_data = pd.concat([opening_month,high_month,low_month,close_month], axis = 1)

cnt = 0
cnt_2 = 0

for i in range(66):
    opens = new_data['open'][i]
    low = new_data['low'][i]
    high = new_data['high'][i]
    close = new_data['close'][i]
    new_low = (opens - (opens/10))
    new_high = (opens + (opens/10))
    
    if(low <= new_low) or (high >= new_high):
        cnt_2 += 1

print(cnt_2)

    
        
