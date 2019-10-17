
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


def MonteCarlo_3(reTime,rf,S,K,sigma): #special for price insurance, whole period price average
	reTime = reTime     #no necessary in this case
	siTi = 1000000
	list = []   #asian put option value list
	dt = 1/360
	totalNodes = reTime
	for si in range(siTi):
		path = [S]
		for node in range(int(totalNodes)-1):
			path.append(path[-1]*exp((rf-0.5*sigma**2)*dt+(sigma*sqrt(dt)*gauss(0,1))))
		if min(path) > 0.97*K:
			executive_price = path[-1]
		elif min(path)>0.935*K:
			executive_price = min(path[-1],0.97*K)
		elif min(path)<0.935*K:
			executive_price = 0.935*K
		asian_put_value = max(K-executive_price,34.1)
		list.append(asian_put_value)
	p = sum(list)/siTi
	return {'asianput ratio:',p/S,
			'asianput value:',p}

# paras input and result
reTime = 60     #remaing days, can be modified in the time structure
rf = .0305     # risk free rate
S = 7583    # current price
K = S    # strike price
sigma = .27    # volatility, mostly the delta of option based on this para
print('remaing time:',reTime)
print('risk free rate:',rf)
print('initial price:',S)
print('target price:',K)
print('*** volatility***',sigma)
timer_ = perf_counter()
print('--------增强亚式   0.97/0.935--------------------')
print(MonteCarlo_3(reTime,rf,S,K,sigma))
print('time cosuming:',perf_counter()-timer_)
timer_ = perf_counter()
