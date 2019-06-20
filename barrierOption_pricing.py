###################################################
# -----------package-----------load-----------######
###################################################

import math
from scipy.stats.distributions import norm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from random import seed, gauss
from math import exp, sqrt, log
import time

p = print

# ---------------------------------------------------------


##########################################################
#### parameters input---#######################
##########################################################


##------------------input
S = 2.336  ##----initial price
X = 2.1  ##------exercise price
T = 30  ##remaing time-------in days
sigma = 0.2  ##volatiltiy based on historical figures
b = 0  ######carry rate
q = 0
r = 0.035  ##---------risk free rate
r = r
H = 2.33  ##----------barrier height
K = 0  #######rebate

putcall = 'p'
inout = 'out'

##########################################
####参数数据结构转化######################
##########################################
sigma = float(sigma)
T = float(T) / 365
r = float(r)
X = float(X)
b = float(b)
H = float(H)
K = float(K)
S = float(S)


#############Function defined for pricing##########
########-----------Method two-------------#########
#####场外期权发展现状及定价研究######################


def price_option_2(S):
    d1 = (-np.log(S / H) - (r - b + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 + sigma * np.sqrt(T)
    d3 = (np.log(S / H) - (r - b - sigma ** 2 / 2) * T / (sigma * np.sqrt(T)))
    d4 = d3 + sigma * np.sqrt(T)
    d5 = (np.log(X / S) - (r - b + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d6 = d5 + sigma * np.sqrt(T)
    d7 = np.log(S * X / H ** 2) - (r - b - sigma ** 2 / 2) * T / sigma * np.sqrt(T)
    d8 = d7 + sigma * np.sqrt(T)

    if putcall == 'c':
        if inout == 'in':
            if S < H:
                price = S * np.exp(-b * T) * (norm.cdf(-d1, 0, 1) - (S / H) ** (-2 / sigma ** 2 * (r - b) - 1) * (
                            norm.cdf(d3, 0, 1) - norm.cdf(d7, 0, 1))) - X * np.exp(-r * T)(
                    norm.cdf(-d2, 0, 1) - (S / H) ** (-2 / sigma ** 2 * (r - q) + 1) * (
                                norm.cdf(d4, 0, 1) - norm.cdf(d8, 0, 1)))
                #####向上敲入看涨期权
            else:
                price = S * np.exp(-b * T) * (S / H) ** (-2 / sigma ** 2 * (r - b) - 1) * norm.cdf(-d7, 0,
                                                                                                   1) - K * np.exp(
                    -r * T) * (S / H) ** (-2 / sigma ** 2 * (r - b) + 1) * norm.cdf(-d8, 0, 1)
                #####向下敲入看涨期权
        else:
            if S < H:
                price = S * np.exp(-b * T) * (
                            norm.cdf(d1, 0, 1) - norm.cdf(d5, 0, 1) - (S / H) ** (-2 / sigma ** 2 * (r - b) - 1) * (
                                norm.cdf(d3, 0, 1) - norm.cdf(d7, 0, 1))) - X * np.exp(-r * T) * (
                                    norm.cdf(d2, 0, 1) - norm.cdf(d6, 0, 1) - (S / H) ** (
                                        -2 / sigma ** 2 * (r - b) + 1) * (norm.cdf(d4, 0, 1) - norm.cdf(d8, 0, 1)))
                #####向上敲出看涨期权
            else:
                price = S * np.exp(-b * T) * (
                            norm.cdf(-d5, 0, 1) - (S / H) ** (-2 / sigma ** 2 * (r - b) - 1) * norm.cdf(-d7, 0,
                                                                                                        1)) - K * np.exp(
                    -r * T) * (-(S / H) ** (-2 / sigma ** 2 * (r - b) + 1) * norm.cdf(-d8, 0, 1) + norm.cdf(-d6, 0, 1))
                #####向下敲出看涨期权
    else:
        if inout == 'in':
            if S < H:
                price = H * np.exp(-r * T) * (S / H) ** (-2 / sigma ** 2 * (r - b) - 1) * norm.cdf(d8, 0,
                                                                                                   1) - S * np.exp(
                    -b * T) * (S / H) ** (-2 / sigma ** 2 * (r - b) - 1) * norm.cdf(d7, 0, 1)
                ####向上敲入看跌期权
            else:
                X * np.exp(-r * T) * (norm.cdf(d2, 0, 1) - (S / H) ** (-2 / sigma ** 2 * (r - b) + 1) * (
                            norm.cdf(d4, 0, 1) - norm.cdf(d8, 0, 1))) - S * np.exp(-b * T)(
                    norm.cdf(d1, 0, 1) - (S / H) ** (-2 / sigma ** 2 * (r - b) - 1) * (
                                norm.cdf(d3, 0, 1) - norm.cdf(d7, 0, 1)))
                ######向下敲入看跌期权
        else:
            if S < H:
                X * np.exp(-r * T) * (norm.cdf(d6, 0, 1) - (S / H) ** (-2 / sigma ** 2 * (r - b) + 1) * norm.cdf(d8, 0,
                                                                                                                 1)) - S * np.exp(
                    -q * T) * (norm.cdf(d5, 0, 1) - (S / H) ** (-2 / sigma ** 2 * (r - b) - 1) * norm.cdf(d7, 0, 1))
                ####向上敲出看跌期权
            else:
                price = X * np.exp(-r * T) * (
                            norm.cdf(d6, 0, 1) - norm.cdf(d2, 0, 1) - (S / H) ** (-2 / sigma ** 2 * (r - q) + 1) * (
                                norm.cdf(d8, 0, 1) - norm.cdf(d4, 0, 1))) - S * np.exp(-q * T) * (
                                    norm.cdf(d5, 0, 1) - norm.cdf(d1, 0, 1) - (S / H) ** (
                                        -2 / sigma ** 2 * (r - q) - 1) * (norm.cdf(d7, 0, 1) - norm.cdf(d3, 0, 1)))
                ####向下敲出看跌期权

    return price


p('price of barrier option-----')
print(price_option_2(S), '------')

#####Standrad European Option Pricing###########
############based on Monte Carlo Method#########


########---------------------------------------#####
########-----------Monte Carlo Method----------#####
########---------------------------------------#####


# ----parameters for monte carlo----------
m = 100000  # m tracks
n = 30  # nodes
dt = T / n
I = 30000
S_list = []
np.random.seed()


def mc_option_price(T, r, S, X, sigma, n, I, m):
    for i in range(I):
        path = []
        for t in range(n + 1):
            if t == 0:
                path.append(S)
            else:
                w = gauss(0, 1)
                St = path[t - 1] * exp((r - 0.5 * sigma ** 2) * dt + sigma * sqrt(dt) * w)
                path.append(St)
        S_list.append(path)
    C0 = exp(-r * T) * sum((max(path[-1] - X, 0) for path in S_list)) / I
    return C0


c = mc_option_price(T, r, S, X, sigma, n, I, m)
print('price of European option------------')
print('based on Monte Carlo Method-')
print(c, '--------')