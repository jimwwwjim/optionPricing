
'''
jimwwwjim

special for price insurance

'''
#----packages input---
#for the historical data
from WindPy import *
w.start()
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

def MonteCarlo_2(reTime,rf,S,K,sigma): #special for price insurance
	reTime = Niter
	siTi = 10
	list_1 = []   #asian call option value list
	list_2 = []   #asian put option value list
	dt = 1/360
	totalNodes = reTime
	for si in range(siTi):
		path = [S]
		for node in range(int(totalNodes)-1):
			path.append(path[-1]*exp((rf-0.5*sigma**2)*dt+(sigma*sqrt(dt)*gauss(0,1))))     
		ave_close = average(path[-30:])
		asian_put_value = max(K-ave_close,0)
		asian_call_value = max(ave_close-K,0)
		list_2.append(asian_put_value)
		list_1.append(asian_call_value)
	p = sum(list_2)/siTi
	c = sum(list_1)/siTi
	#return {'asianput_MC':p,'asiancall_MC':c,'asiandelta':delta,'asian_gamma':gamma}
	return {'asianput_MC':p,'asiancall_MC':c}

timer_ = clock()
print(MonteCarlo(28,.03,12030,12030,.3),clock()-timer_)