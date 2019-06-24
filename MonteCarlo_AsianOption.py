
'''
jimwwwjim

special for price insurance

'''
#----packages input---

import numpy as np
from math import exp, sqrt
from random import seed, gauss
import datetime
from time import clock, perf_counter



def MonteCarlo_1(reTime,rf,S,K,sigma): #special for price insurance, last 30 days average price
	reTime = reTime     #no necessary in this case
	siTi = 100000
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
	return {'asianput_MC':p,'asiancall_MC':c}

def MonteCarlo_2(reTime,rf,S,K,sigma): #special for price insurance, whole period price average
	reTime = reTime     #no necessary in this case
	siTi = 100000
	list_1 = []   #asian call option value list
	list_2 = []   #asian put option value list
	dt = 1/360
	totalNodes = reTime
	for si in range(siTi):
		path = [S]
		for node in range(int(totalNodes)-1):
			path.append(path[-1]*exp((rf-0.5*sigma**2)*dt+(sigma*sqrt(dt)*gauss(0,1))))
		ave_close = np.average(path)
		asian_put_value = max(K-ave_close,0)
		asian_call_value = max(ave_close-K,0)
		list_2.append(asian_put_value)
		list_1.append(asian_call_value)
	p = sum(list_2)/siTi
	c = sum(list_1)/siTi
	return {'asianput_MC':p,'asiancall_MC':c}


# paras input and result
reTime = 120     #remaing days, can be modified in the time structure
rf = .03     # risk free rate
S = 12030     # current price
K = 12030     # strike price
sigma = .3    # volatility
timer_ = perf_counter()
print('--------最后三十天取平均值--------------------')
print(MonteCarlo_1(reTime,rf,S,K,sigma), perf_counter()-timer_)
timer_ = perf_counter()
print('--------整个阶段取平均值--------------------')
print(MonteCarlo_2(reTime,rf,S,K,sigma), perf_counter()-timer_)