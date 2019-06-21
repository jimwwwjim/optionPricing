
'''

分阶段期权

先看涨后看跌



author：JIMWWWJIM



'''



#4个月两个阶段先看涨后看跌取平均

#--------package
import numpy as np
import pandas as pd
from random import seed,gauss
from math import exp, sqrt, log
import time




#----------parameters
s0 = 11500    #initial price
sigma = 0.3    #volatility
r = 0.0278
print('无风险利率  ', r)
dt = 1/360
min_pay = 30


#---method one
#----calculation

#求list平均值

def averagenum(num):
	nsum = 0
	for i in range(len(num)):
		nsum += num[i]
	return nsum/len(num)


N = 2
I = 1000000
M = 30
option_value_list = []
option_1_list = []
option_2_list = []
Per = N*M
q = 0

for i in range(I):
	option_value = 0
	for n in range(N):
		if n == 0:
			S0 = s0
		else:
			S0 = path_1[-1]
		path = []
		for m in range(M):
			if m == 0:
				path.append(S0)
			else:
				w = gauss(0,1)
				St = path[m-1]*exp((r-0.5*sigma**2)*dt+sigma*sqrt(dt)*w)
				path.append(St)
		path_1 = path
		#if n == 0:
			#option_value = option_value + max((averagenum(path)-S0),0)*exp(-r*(n+1)/12)
			#print('第一阶段看涨期权     ',max((averagenum(path)-S0),0)*exp(-r*(n+1)/12))
		#else:
			#option_value = option_value + max((S0-averagenum(path)),0)*exp(-r*(n+1)/12)
			#print('第二阶段看跌期权     ', max((S0-averagenum(path)),0)*exp(-r*(n+1)/12))
		option_value = option_value + max((S0-averagenum(path)),0)*exp(-r*(n+1)/12)
		if n == 0:
			option_1_list.append(option_value)
	if option_value < min_pay:
		q = q + 1
	option_value_list.append(max(option_value,min_pay))

print('触碰次数    ',q)
print('触碰',min_pay,'比率    ',q/I)
print('current price of RU.SHF   ', s0)
print('总天数     ', Per)
print('模拟次数     ', I)     
print('阶段数   ', N)
print('分阶段期权,   ',sum(option_value_list)/I)
print('分阶段第一阶段', sum(option_1_list)/I)
print('分阶段第二阶段', sum(option_value_list)/I-sum(option_1_list)/I)
print('成本比率    ',sum(option_value_list)/I/s0)