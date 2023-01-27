# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 18:42:09 2023

@author: riyas
"""
#we need to sell call and put at the same strike price
#then put stop loss of 30 points
#End trade at the end of day

#on selling call we will have profit when the price moves down
#on selling put we will have profit when the price moves up

#rough code on one particular CE, PE for 18000

import pandas as pd
import pickle

df = pd.read_pickle(r"C:\Users\riyas\Downloads\NIFTY22JAN18000PE.pkl")
ef = pd.read_pickle(r"C:\Users\riyas\Downloads\NIFTY22JAN18000CE.pkl")

df['datetime'] = df['Date'] +" " + df['Time']
ef['datetime'] = ef['Date'] +" " + ef['Time']
#df.drop(columns = ['datetime'], axis = 1, inplace = True)
df.set_index(df.datetime, inplace = True)
ef.set_index(ef.datetime, inplace = True)

df.index = pd.to_datetime(df.index)
ef.index = pd.to_datetime(ef.index)

def resample_data(df):
    opening=df.resample('D',origin= 'start').first()
    opening.drop(['High','Low','Close','Volume','Symbol','OI','Expiry','OptionType','Date','Time','Strike','datetime'],axis=1,inplace=True)

    high=df.resample('D',origin= 'start').max()
    high.drop(['Open','Low','Close','Volume','Symbol','OI','Expiry','OptionType','Date','Time','Strike','datetime'],axis=1,inplace=True)

    low=df.resample('D',origin= 'start').min()
    low.drop(['Open','High','Close','Volume','Symbol','OI','Expiry','OptionType','Date','Time','Strike','datetime'],axis=1,inplace=True)

    close=df.resample('D',origin= 'start').last()
    close.drop(['Open','Low','High','Volume','Symbol','OI','Expiry','OptionType','Date','Time','Strike','datetime'],axis=1,inplace=True)

    df_new = pd.concat([opening,high,low,close], axis = 1)
    df_new.dropna(inplace = True)
    
    return df_new

df_new = resample_data(df)
ef_new = resample_data(ef)

profit = 0

for i in range(76):
    if(df_new['High'][i] >= 1.3*df_new['Open'][i]):
        profit -= 0.3*df_new['Open'][i]
    elif(df_new['High'][i] < 1.3*df_new['Open'][i]):
        profit += (df_new['Close'][i] - df_new['Open'][i])
    
    if(ef_new['Low'][i] <= 0.7*ef_new['Open'][i]):
        profit -= 0.3*df_new['Open'][i]
    elif(df_new['Low'][i] > 0.7*ef_new['Open'][i]):
        profit += (ef_new['Close'][i] - ef_new['Open'][i])
        
        
        
        