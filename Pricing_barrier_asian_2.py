'''

带特殊障碍条款的亚式

最低赔付：30

author：JIMWWWJIM

整个阶段的平均值或最后一个月的平均值

大体结构与 Pricing_barrier_asian.py相同，再次不赘述
'''


#---------package
import numpy as np
import pandas as pd
from random import seed,gauss
from math import exp, sqrt, log
from time import perf_counter
from scipy.stats.distributions import norm

s0_C = 1986     # C.DCE 当前价格水平
s0_A = 3400     # A.DCE 当前价格水平
sigma_C = 0.1   # C.DCE 当前HV50的中值
sigma_A = 0.18  # A.DCE 当前HV30的最新值
N = 1
M = 120          #期限长度是4个月
min_pay = 30
Per = N*M
option_value_list = []


def BS_option_price(S0,K,sigma,T):
	d1 = (np.log(S0/K)+(rf+sigma**2/2)*T)/sigma*np.sqrt(T)
	d2 = d1 - sigma*np.sqrt(T)
	c = S0*norm.cdf(d1,0,1)-K*np.exp(-rf*T)*norm.cdf(d2,0,1)
	p = K*np.exp(-rf*T)*norm.cdf(-d2,0,1)-S0*norm.cdf(-d1,0,1)
	return {'BS_call':c,'BS_put':p}

def MonteCarlo_1(reTime,rf,S,K,sigma): #special for price insurance, last 30 days average price
	reTime = reTime     #no necessary in this case
	siTi = 100000
	list_1 = []   #asian call option value list
	list_2 = []   #asian put option value list
	dt = 1/360
	a = 0
	b = 0
	totalNodes = reTime
	for si in range(siTi):
		path = [S]
		for node in range(int(totalNodes)-1):
			path.append(path[-1]*exp((rf-0.5*sigma**2)*dt+(sigma*sqrt(dt)*gauss(0,1))))
		ave_close = np.average(path[-30:])
		asian_put_value = max(max(K-ave_close,0),30)      #最低赔付30
		if max(K-ave_close,0) < 30:
			a = a + 1
		asian_call_value = max(max(ave_close-K,0),30)     #最低赔付30
		if max(ave_close-K,0) > 30:
			b = b + 1
		list_2.append(asian_put_value)
		list_1.append(asian_call_value)
	p = sum(list_2)/siTi
	c = sum(list_1)/siTi
	return {'asianput_MC':p,'asianput_minrate':a/siTi,'asiancall_MC':c,'asiancall_minrate':b/siTi}

def MonteCarlo_2(reTime,rf,S,K,sigma): #special for price insurance, whole period price average
	reTime = reTime     #no necessary in this case
	siTi = 100000
	list_1 = []   #asian call option value list
	list_2 = []   #asian put option value list
	a = 0
	b = 0
	dt = 1/360
	totalNodes = reTime
	for si in range(siTi):
		path = [S]
		for node in range(int(totalNodes)-1):
			path.append(path[-1]*exp((rf-0.5*sigma**2)*dt+(sigma*sqrt(dt)*gauss(0,1))))
		ave_close = np.average(path)
		asian_put_value = max(max(K-ave_close,0),30)      #最低赔付30
		if max(K-ave_close,0) < 30:
			a = a + 1
		asian_call_value = max(max(ave_close-K,0),30)     #最低赔付30
		if max(ave_close-K,0) > 30:
			b = b + 1
		list_2.append(asian_put_value)
		list_1.append(asian_call_value)
	p = sum(list_2)/siTi
	c = sum(list_1)/siTi
	return {'asianput_MC':p,'asianput_minrate':a/siTi,'asiancall_MC':c,'asiancall_minrate':b/siTi}


T = Per/360
dt = 1/360
rf = 0.03
I = 1000000
reTime = Per


print('最低赔付    ',min_pay)
print('总天数     ', Per)
print('模拟次数     ', I)
print('--------------A.DCE-------------')
S = s0_A
K = s0_A
sigma = sigma_A
print('----------BS option Prices------')
print(BS_option_price(S, K, sigma, T))
print('---------最后三十天取平均值---')
timer_ = perf_counter()
print(MonteCarlo_1(reTime,rf,S,K,sigma), perf_counter()-timer_)
print('--------整个阶段取平均值--------------------')
timer_ = perf_counter()
print(MonteCarlo_2(reTime,rf,S,K,sigma), perf_counter()-timer_)
print('--------------C.DCE-------------')
S = s0_C
K = s0_C
sigma = sigma_C
print('-------------BS option Prices---------------')
print(BS_option_price(S, K, sigma, T))
print('------------最后三十天取平均值--------------')
timer_ = perf_counter()
print(MonteCarlo_1(reTime,rf,S,K,sigma), perf_counter()-timer_)
print('------------整个阶段取平均值-----------------')
timer_ = perf_counter()
print(MonteCarlo_2(reTime,rf,S,K,sigma), perf_counter()-timer_)
print('--------------------------------------------')