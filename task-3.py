# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 12:13:08 2023

@author: riyas
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation

#reading the xlxs file
df = pd.read_excel(r"C:\Users\riyas\Downloads\230123.xlsx")

#given tokens according to which we need to diffrentiate
tk_1 = 14211586
tk_2 = 8972290
tk_3 = 8972034

#df1, df2, and df3 are the dataframes for token-1,2 and 3
df1 = df.loc[df.token == tk_1]
df1.reset_index(inplace = True)

df2 = df.loc[df.token == tk_2]
df2.reset_index(inplace = True)

df3 = df.loc[df.token == tk_3]
df2.reset_index(inplace = True)

#list created for the grpah plotting as a whole(not dynamically)
#x axis will contain the time 
#y axis will contain the price
y = df1['price'][:]
x = df1['time'][:]

plt.plot(x,y)
plt.show()

#dynamic drawing of graph
count = 0
x1 = []
y1 = []

#this will reaload values after re-running everytime
def draw_graph(i):
    global count
    count += 1
    x1.append(df1['time'][count])
    y1.append(df1['price'][count])
    
    plt.cla()
    plt.plot(x1,y1)

anim = animation.FuncAnimation(plt.gcf(),draw_graph,interval = 1500)

    
count_2 = 0
x2 = []
y2 = []

def draw_graph_2(i):
    global count_2
    count_2 += 1
    x2.append(df2['time'][count_2])
    y2.append(df2['price'][count_2])
    
    plt.cla()
    plt.scatter(x2,y2)
    plt.plot(x2,y2)

anims = animation.FuncAnimation(plt.gcf(),draw_graph_2,interval = 1500)

count_3 = 0
x3 = []
y3 = []

def draw_graph_3(i):
    global count_3
    count_3 += 1
    x3.append(df3['time'][count_3])
    y3.append(df3['price'][count_3])
    
    plt.cla()
    plt.scatter(x3,y3)
    plt.plot(x3,y3)

animse = animation.FuncAnimation(plt.gcf(),draw_graph_3,interval = 1500)
    