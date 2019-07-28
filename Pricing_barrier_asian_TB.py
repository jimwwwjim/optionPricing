




import numpy as np
#from WindPy import *
import sys
import os
#print(sys.path)
import pandas as pd
from random import seed,gauss
from math import exp, sqrt, log
from time import perf_counter
from scipy.stats.distributions import norm
#w.start()
s0_C = 1991     # C2001.DCE 当前价格水平
sigma_C = 0.099   # C.DCE 当前HV50的中值
print('initial price of C.DCE:',s0_C,'sigma of C.DCE:',sigma_C)



N = 4
M = 30          #期限长度是4个月
min_pay = 30
Per = N*M
option_value_list = []
T = Per/360
dt = 1/360
rf = 0.035 #0.02467
print('risk free rate:',rf)
I = 100000
reTime = Per
timer_ = perf_counter()
#print( MonteCarlo_3(reTime,rf,S,K,sigma), perf_counter()-timer_)



def MonteCarlo_5(reTime,rf,S,K,sigma,min_pay):
	reTime = reTime     #no necessary in this case
	siTi = 100000
	list_1 = []    #asian call option value list
	list_2 = []   #asian put option value list
	list_3=[]
	list_4=[]
	dt = 1/360
	a = 0
	totalNodes = reTime
	for si in range(siTi):
		path = [S]
		for node in range(int(totalNodes)-1):
			path.append(path[-1]*exp((rf-0.5*sigma**2)*dt+(sigma*sqrt(dt)*gauss(0,1))))
		'''
		增强亚式
		last30
		'''
		path_last30 = []   #for put
		path_last30_ = []  #for call
		for st in path[-30:]:
			if st > K:
				path_last30.append(K)
			elif st<= K:
				path_last30.append(st)
		for st_ in path[-30:]:
			if st_>K:
				path_last30_.append(st)
			elif st_<= K:
				path_last30_.append(K)
		ave_close = np.average(path_last30)
		ave_close_ = np.average(path_last30_)
		asian_put_value = max(max(K-ave_close,0),min_pay)      #增强看跌期权
		asian_call_value = max(max(ave_close_-K,0),min_pay)       #增强看涨期权
		'''
		普通亚式
		'''
		asian_put_value_ = max(max(K-np.average(path[-30:]),0),min_pay)#普通看跌
		asian_call_value_ = max(max(np.average(path[-30:])-K,0),min_pay)  #普通看涨
		list_1.append(asian_call_value)
		list_2.append(asian_put_value)


		list_3.append(asian_put_value_)
		list_4.append(asian_call_value_)
	c = np.average(list_1)
	p = sum(list_2)/siTi
	c_ = np.average(list_4)
	p_ = np.average(list_3)
	return {'普通亚式看跌':p_,'普通亚式看涨':c_}


S = s0_C
K = S
sigma = sigma_C
min_pay = 23
print('最低赔付：',min_pay)

print(MonteCarlo_5(reTime,rf,S,K,sigma,min_pay))