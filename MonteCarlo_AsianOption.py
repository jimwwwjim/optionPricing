
'''
jimwwwjim

special for price insurance

'''
#----packages input---
#for the historical data
#from WindPy import *           no Wind Terminal needed in this case
#w.start()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import exp, sqrt, log
from random import seed, gauss
import datetime
from time import clock
from scipy.stats.distributions import norm
import scipy
# pd setting
pd.set_option('display.width',320)
pd.set_option('display.max_rows',100)
# historical data collection and management
# minutes data based on wsi api function

#time structure
contract_enddate = '2019-06-30'
contract_startdate = '2019-05-31'
def time_remain(contract_enddate):
    t_end = datetime.datetime.strptime(contract_enddate,'%Y-%m-%d')
    date_end = t_end.date()
    date_now = datetime.datetime.now().date()
    time_delta = date_end - date_now
    re_days = time_delta.days
    T = re_days/365
    return re_days,T
remain_days, remain_T = time_remain(contract_enddate)
itertype = '1day'
t_start = datetime.datetime.strptime(contract_startdate,'%Y-%m-%d')
t_end = datetime.datetime.strptime(contract_enddate,'%Y-%m-%d')
t_delta = t_end - t_start
print(t_delta)

dt = 0     #相邻节点之间的距离
Niter = 0   #总结点的选择
if itertype == '1day':
    dt = 1/360
    Niter = t_delta.days
    print(Niter)
elif itertype == '30min':
    dt = 1/3000        # waiting for modification
    Niter = t_delta.days*12
elif itertype == '1hour':
    dt = 1/1500       # waiting for modification
    Niter = t_delta.days*6

def MonteCarlo(reTime,rf,S,K,sigma): #special for price insurance
	reTime = Niter     #no necessary in this case 
	siTi = 10
	list_1 = []   #asian call option value list
	list_2 = []   #asian put option value list
	dt = 1/360
	totalNodes = reTime
	for si in range(siTi):
		path = [S]
		for node in range(int(totalNodes)-1):
			path.append(path[-1]*exp((rf-0.5*sigma**2)*dt+(sigma*sqrt(dt)*gauss(0,1))))     
		ave_close = np.average(path[-30:])
		asian_put_value = max(K-ave_close,0)
		asian_call_value = max(ave_close-K,0)
		list_2.append(asian_put_value)
		list_1.append(asian_call_value)
	p = sum(list_2)/siTi
	c = sum(list_1)/siTi
	#return {'asianput_MC':p,'asiancall_MC':c,'asiandelta':delta,'asian_gamma':gamma}
	return {'asianput_MC':p,'asiancall_MC':c}


# paras input and result
reTime = 28     #remaing days, can be modified in the time structure
rf = .03     # risk free rate
S = 12030     # current price
K = 12030     # strike price
sigma = .3    # volatility
timer_ = clock()
print(MonteCarlo(reTime,rf,S,K,sigma),clock()-timer_)