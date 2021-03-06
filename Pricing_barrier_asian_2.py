'''

带特殊障碍条款的亚式

最低赔付：30

author：JIMWWWJIM

整个阶段的平均值或最后一个月的平均值

大体结构与 Pricing_barrier_asian.py相同，再次不赘述
'''


#---------package
import numpy as np
#from WindPy import *
import sys
import os
print(sys.path)
import pandas as pd
from random import seed,gauss
from math import exp, sqrt, log
from time import perf_counter
from scipy.stats.distributions import norm
#w.start()

s0_C = 1981     # C2001.DCE 当前价格水平
print('initial price of C.DCE:',s0_C)
s0_A = 3399     # A.DCE 当前价格水平
print('initial price of A.DCE:',s0_A)
s0_M = 2836      # M2001.DCE 当前价格水平
print('initial price of M.DCE:',s0_M)
s0_JD = 4158   # JD.DCE 当前价格水平
sigma_C = 0.11   # C.DCE 当前HV50的中值
print('sigma of C.DCE:',sigma_C)
sigma_A = 0.20  # A.DCE 当前HV30的最新值
print('sigma of A.DCE',sigma_A)
sigma_M = 0.17    # M.DCE    当前最新HV50
print('sigma of M.DCE:',sigma_M)
sigma_JD = 0.19   #JD.DCCE 当前hv
print('sigma of JD.DCE:', sigma_JD)
min_pay_C = 25
min_pay_A = 40
min_pay_M = 0
min_pay_JD = 0
print('min pay for C.DCE:',min_pay_C)
print('min pay for A.DCE:',min_pay_A)
print('min pay for JD.DCE:',min_pay_JD)

barrier_C = s0_C*1.075  # 预设定   C.DCE 敲入或敲出价格
print('barrier price of C.DCE:',barrier_C)
barrier_M = s0_M*1.04  # 预设定   M.DCE 敲入或敲出价格
print('barrier price of M.DCE:', barrier_M) 

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

'''
# data collection
wsd_data = w.wsd('A2001.DCE','close','2019-06-15','2019-07-01','')
close_data = wsd_data.Data[0]
'''



def BS_option_price(S0,K,sigma,T):
	d1 = (np.log(S0/K)+(rf+sigma**2/2)*T)/sigma*np.sqrt(T)
	d2 = d1 - sigma*np.sqrt(T)
	c = S0*norm.cdf(d1,0,1)-K*np.exp(-rf*T)*norm.cdf(d2,0,1)
	p = K*np.exp(-rf*T)*norm.cdf(-d2,0,1)-S0*norm.cdf(-d1,0,1)
	return {'BS_call':c,'BS_put':p}

def MonteCarlo_1(reTime,rf,S,K,sigma,min_pay): #special for price insurance, last 30 days average price
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
		asian_put_value = max(max(K-ave_close,0),min_pay)      #最低赔付
		if max(K-ave_close,0) < min_pay:
			a = a + 1
		asian_call_value = max(max(ave_close-K,0),min_pay)     #最低赔付
		if max(ave_close-K,0) > min_pay:
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


def MonteCarlo_3(reTIme,rf,S,K,sigma,N,M):
	N = N
	M = M
	siTi = 100000
	list_1 = []   #asian call option value list
	list_2 = []   #asian put option value list
	dt = 1/360
	a = 0
	b = 0
	for si in range(siTi):
		call_value = 0
		put_value = 0
		for n in range(N):
			if n == 0:
				s0 = S
			else:
				s0 = path[-1]
			path = []
			for m in range(M):
				if m == 0:
					path.append(s0)
				else:
					path.append(path[m-1]*exp((rf-0.5*sigma**2)*dt+sigma*sqrt(dt)*gauss(0,1)))
			put_value = put_value + max((s0-np.average(path)),0)*exp(-rf*(n/12))
		list_2.append(put_value)
	return {'分阶段亚式看跌期权：':np.average(list_2),'总阶段数：':N}



def MonteCarlo_4(reTime,rf,S,K,sigma,barrier_): #special for price insurance, last 30 days average price  #barrier price needed
	reTime = reTime     #no necessary in this case
	siTi = 100000
	list_1 = []   #asian call option value list
	list_2 = []   #asian put option value list
	dt = 1/360
	a = 0
	totalNodes = reTime
	for si in range(siTi):
		path = [S]
		for node in range(int(totalNodes)-1):
			path.append(path[-1]*exp((rf-0.5*sigma**2)*dt+(sigma*sqrt(dt)*gauss(0,1))))
		if max(path)<barrier_:
			value = 0
		elif max(path)>=barrier_:
			value = barrier_ - S
			a = a + 1
		list_1.append(value)
	c = sum(list_1)/siTi
	return {'二元触碰期权价格：':c,'触碰概率':a/siTi}


'''
S = s0_A
K = s0_A
sigma = sigma_A



print('最低赔付    ',min_pay)
print('总天数     ', Per)
print('模拟次数     ', I)

print('--------------M.DCE-------------')
S = s0_M
K = s0_M
sigma = sigma_M
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
barrier_ = barrier_C
sigma = sigma_C
min_pay = 36

print('-------------BS option Prices---------------')
print(BS_option_price(S, K, sigma, T))
print('--------二元触碰期权-------')
print(MonteCarlo_4(reTime,rf,S,K,sigma,barrier_))


print('------------最后三十天取平均值--------------')
timer_ = perf_counter()
print(MonteCarlo_1(reTime,rf,S,K,sigma,min_pay), perf_counter()-timer_)

print('------------整个阶段取平均值-----------------')
timer_ = perf_counter()
print(MonteCarlo_2(reTime,rf,S,K,sigma), perf_counter()-timer_)
print('--------------------------------------------')
print('--------------M.DCE-------------')
S = s0_M
K = s0_M
sigma = sigma_M
barrier_ = barrier_M
min_pay = 40
print('----------BS option Prices------')
print(BS_option_price(S, K, sigma, T))
print('--------二元触碰期权-------')
print(MonteCarlo_4(reTime,rf,S,K,sigma,barrier_))
print('---------最后三十天取平均值---')
timer_ = perf_counter()
print(MonteCarlo_1(reTime,rf,S,K,sigma,min_pay), perf_counter()-timer_)
print('--------整个阶段取平均值--------------------')
timer_ = perf_counter()
print(MonteCarlo_2(reTime,rf,S,K,sigma), perf_counter()-timer_)
'''
S= s0_JD
K = S
sigma = sigma_JD
print('-------------JD.DCE--------------')
print('-------分阶段看跌亚式-------------')
print(MonteCarlo_3(reTime,rf,S,K,sigma,N,M))
