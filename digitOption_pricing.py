
'''
author : jimwwwjim

for digit option pricing
'''


#packages input
import numpy as np
from scipy.stats.distributions import norm
from math import exp, sqrt, log
from random import seed, gauss
import datetime
from time import clock, perf_counter


#parameters settings
s0 = 8245     #initial price 起始价
S = s0
K = s0        #strike price 到期价
max_payment = 450    #最高赔付
Q = max_payment
r = 0.03      #risk free rate无风险利率
sigma = 0.16  #sigma or volatility波动率
startdate = '2019-06-27'
enddate = '2019-07-27'
T = (datetime.datetime.strptime(enddate,'%Y-%m-%d') - datetime.datetime.strptime(startdate,'%Y-%m-%d')).days/360 #30天

#method one
#closed form solution

def BS_digitOptionPricing(S,K,Q,r,sigma,T):
    d2 = (log(S/K)+(r - 0.5*sigma**2)*T)/(sigma*sqrt(T))
    c = Q*exp(-r*T)*norm.cdf(d2,0,1)
    p = Q*exp(-r*T)*norm.cdf(-d2,0,1)
    return c,p

c,p = BS_digitOptionPricing(S,K,Q,r,sigma,T)
print('--------------------------------')
print('---based on closed form---------')
print('-------二元期权看涨价格---------')
print(c)
print('-------二元期权看跌价格---------')
print(p)
print('--------------------------------')





