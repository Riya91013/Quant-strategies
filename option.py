#implementing the black-scholes formula in python

import numpy as np
from scipy.stats import norm

#define variables
# r as interest rate ,s as underline, k as strike price, t as time, sigma for volatility
r = 0.01
s = 30
K = 40
T = 240/365
sigma = 0.3

def blackscholes(r,s,K,T,sigma,type = 'C'):
    # Calculating BS option price for a call/put
    d1 = (np.log(s/K) + (r+ sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try:
        if type == "C":
            price = s*norm.cdf(d1,0,1) - K*np.exp(-r*T)*norm.cdf(d2,0,1)
        elif type == "P":
            price = K*np.exp(-r*T)*norm.cdf(-d2,0,1) - s.norm.cdf(-d1,0,1)
        return price
    except:
        print("Please confirm all option parameters above!!!")

print("Option Price is: ", round(blackscholes(r,s,K,T,sigma,type = "C"),2))
