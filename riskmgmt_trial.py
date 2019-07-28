

from math import sqrt,log,exp
import numpy as np
from random import gauss
import pandas as pd

s0 = 1991
sigma = 0.0791
rf = 0.0305
S = s0
K = S
days = 122
T = days/360

I = 1000000
dt = 1/360




def MonteCarlo(S,K,T,sigma):
    put_value_list = []
    put_value_list_ = []
    for i in range(I):
        path=[S]
        for day in range(days-1):
            path.append(path[-1]*exp((rf-0.5*sigma**2)*dt+sigma*sqrt(dt)*gauss(0,1)))
        #全阶段亚式期权
        ave_close = np.average(path)
        put_value = max(K - ave_close,0)
        #最后三十天增强式
        path_30 = []
        for p in path[-30:]:
            if p < K:
                path_30.append(p)
            else:
                path_30.append(K)
        ave_close_ = np.average(path_30)
        put_value_ = max(K - ave_close_,0)
        put_value_list.append(put_value)
        put_value_list_.append(put_value_)
    print('全阶段亚式期权价值:  ',np.average(put_value_list))
    print('全阶段期权费率',np.average(put_value_list)/S)
    print('最后三十天增强亚式： ',np.average(put_value_list_))
    print('最后三十天期权费率:  ',np.average(put_value_list_)/S)
    df = pd.DataFrame({'全阶段亚式期权价值':put_value_list,'最后三十天增强亚式':put_value_list_})
    print(df.head(20))
    print('75%分位数'
          ,df.quantile(q=0.75))
    a = df.quantile(q=0.75)['全阶段亚式期权价值']
    b = df.quantile(q=0.75)['最后三十天增强亚式']
    print('全阶段期权多头收益率：',a/S)
    print('最后三十天期权多头收益率；',b/S)
    print('90%分位数'
          ,df.quantile(q=0.9))
    a = df.quantile(q=0.9)['全阶段亚式期权价值']
    b = df.quantile(q=0.9)['最后三十天增强亚式']
    print('全阶段期权多头收益率：',a/S)
    print('最后三十天期权多头收益率；',b/S)
    print('95%分位数'
          ,df.quantile(q=0.95))
    a = df.quantile(q=0.95)['全阶段亚式期权价值']
    b = df.quantile(q=0.95)['最后三十天增强亚式']
    print('全阶段期权多头收益率：',a/S)
    print('最后三十天期权多头收益率；',b/S)
    print('99%分位数'
          ,df.quantile(q=0.99))
    a = df.quantile(q=0.99)['全阶段亚式期权价值']
    b = df.quantile(q=0.99)['最后三十天增强亚式']
    print('全阶段期权多头收益率：',a/S)
    print('最后三十天期权多头收益率；',b/S)


MonteCarlo(S,K,T,sigma)

