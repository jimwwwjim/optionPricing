'''

带特殊障碍条款的亚式

障碍触碰线： 400

当移动平均值触碰到障碍线时，出现最低赔付的限制条款

author：JIMWWWJIM

移动平均线在存续期开始后10天开始计算

'''
#---------package loaded-----------
import numpy as np
import pandas as pd
from random import seed,gauss
from math import exp, sqrt, log
import time
from scipy.stats.distributions import norm
#------ BS pricing function---
#------using the price based on BS model as basic 
def BS_option_price(S0,K,sigma,T):
	d1 = (np.log(S0/K)+(r+sigma**2/2)*T)/sigma*np.sqrt(T)
	d2 = d1 - sigma*np.sqrt(T)
	c = S0*norm.cdf(d1,0,1)-K*np.exp(-r*T)*norm.cdf(d2,0,1)
	p = K*np.exp(-r*T)*norm.cdf(-d2,0,1)-S0*norm.cdf(-d1,0,1)
	return c,p 
#--------parameters setting-----
s0 = 11500
N = 1      #分阶段期权可用
M = 60
Per = N*M   #总节点， total nodes, 60days in this case
ma = 10     #10 日移动平均
ma_ext = int(ma / 2)
option_value_list = []
min_pay = 30   # required minimum pay

S0 = s0     #期初价格
K = s0      #执行价为期初价格
T = 1/6     #total time
sigma = 0.38#volatiltiy
r = 0.03    #risk free rate
#print('无风险利率  ', r)
I = 1000000  #经实证，模拟次数达到100,000次时，结果开始趋于稳定，这里使用1,000,000较为保险
dt = 1/360   #delta time， each node means one day 每个节点代表一天
c,p = BS_option_price(S0,K,sigma,T)
cpflag = 'p'   # if the option is a kind of put then take it as 'p', call? 'c'
q = 0       #不存在鼓励分发
b = 0       #触碰后，不存在返还


# ------- MC simulations-------
#---------For I paths----------

for i in range(I):
	option_value = 0
	path = []
	ma10 = []
	for per in range(Per):
		if per == 0:
			path.append(s0)
		else:
			St = path[per-1]*exp((r-0.5*sigma**2)*dt+sigma*sqrt(dt)*gauss(0,1))
			path.append(St)
	ave_close = sum(path)/len(path)
	df_1 = pd.DataFrame(path)
	ma10 = df_1.rolling(window=10).mean().dropna()
	ma10_list = ma10.values.tolist()
	min_ma10 = min(ma10_list)[0]
	max_ma10 = max(ma10_list)[0]
	if cpflag == 'c':
		mu = max_ma10 - S0
		if mu >400:
			b = b + 1
			ex_price = max(S0+400,ave_close)
		else:
			ex_price = ave_close
		option_value = max(ex_price-S0,min_pay)
	elif cpflag == 'p':
		mu = S0 - min_ma10
		if mu > 400:
			b = b + 1
			ex_price = min(S0-400,ave_close)
		else:
			ex_price = ave_close
		option_value = max(S0-ex_price,min_pay)
	if abs(S0-ex_price) < min_pay:
		q = q + 1
	option_value_list.append(option_value)
#---------results print out-------
print('触碰',min_pay,'比率   ',q/I)
print('触碰 400 比率   ', b/I)
print('最低赔付    ',min_pay)
print('current price of RU.SHF   ', s0)
print('总天数     ', Per)
print('模拟次数     ', I) 
print('带特殊条款的亚式期权价值     ',sum(option_value_list)/I)
print('成本比率     ',sum(option_value_list)/I/S0)
