
'''
waiting for further edition
'''




class Vanilla_BAW(Vanilla):
    '''
    类初始化函数，定义了计算所需的中间变量和初始化参数
    '''


def __init__(self):
    self.spot = None  # 标的价格
    self.strike = None  # 执行价
    self.volatility = None  # 波动率
    self.div_rate = 0  # 股息率

    self.option_type = None  # 期权类型
    self.rate = None  # 无风险利率
    self.gap = None  # 期权到期时间-期权开始时间，以年为单位
    self.calc_time = None  # 期权起始时间
    self.maturity_time = None  # 期权到期时间
    self.dF = None  # 使用无风险利率的折现因子

    self.d1 = None  # 欧式期权BSM公式中的d1
    self.d2 = None  # 欧式期权BSM公式中的d2
    self.Euro_CALL_NPV = None  # 欧式call期权价格
    self.Euro_PUT_NPV = None  # 欧式put 期权价格

    # 定义了美式期权计算所需的中间变量

    self.q1 = None
    self.q2 = None
    self.A1 = None
    self.A2 = None
    self.N = None
    self.M = None
    self.X = None
    self.spot_star = None

    self.NPV = None  # 美式期权价格
    return

    def set_parameters(self, Stock, K, rate,t, T, sigma, type):
        self.spot = Stock
        self.strike = K * Stock
        self.rate = rate

        self.calc_time = t
        self.maturity_time = T
        self.gap = T - t

        self.volatility = sigma
        self.option_type = type

        return

    # 计算累积正态分布
    def __N__(self, d):
        return ss.norm.cdf(d)

    # BSM公式中的d1和d2
    def __d1_d2__(self, S):

        '''
        计算带有股息率的d1,d2
        :param S: 期初价格
        :return:
        '''

        d1 = (log(S / self.strike) +
              (self.rate - self.div_rate + 0.5 * self.volatility ** 2) *
              self.gap) / (self.volatility * sqrt(self.gap))

        d2 = d1 - self.volatility * sqrt(self.gap)

        return d1, d2

    # 计算欧式看涨
    def __Euro_call__(self, S):
        d1, d2 = self.__d1_d2__(S)
        Euro_NPV = S * exp(-self.div_rate * self.gap) * self.__N__(d1) \
                   - exp(-self.rate * self.gap) * self.strike * self.__N__(d2)

        return Euro_NPV

    # 计算欧式看跌
    def __Euro_put__(self, S):
        d1, d2 = self.__d1_d2__(S)
        Euro_NPV = self.strike * exp(-self.rate * self.gap) * self.__N__(-d2) \
                   - S * exp(-self.div_rate * self.gap) * self.__N__(-d1)

        return Euro_NPV

    def __q__(self):
        self.M = 2 * self.rate / (self.volatility ** 2)
        self.N = 2 * (self.rate - self.div_rate) / (self.volatility ** 2)
        self.X = 1 - exp(-self.rate * self.gap)

        self.q1 = (-(self.N - 1) - sqrt((self.N - 1) ** 2 + 4 * self.M / self.X)) / 2
        self.q2 = (-(self.N - 1) + sqrt((self.N - 1) ** 2 + 4 * self.M / self.X)) / 2

        return

    # 定义不同类型期权的Sx值
    def __func_spot_star__(self, Sx):

        if Sx < 0:
            return 1e1000

        if self.option_type == 'CALL':
            value1 = self.__Euro_call__(Sx)  # c(S，T)
            value2 = exp(-self.div_rate * self.gap)
            value3 = (1 - value2 * self.__N__(self.__D1_Postive__(Sx))) * Sx / self.q2
            y = (value1 + value3 - Sx + self.strike) ** 2
            return y

        if self.option_type == 'PUT':
            value1 = self.__Euro_put__(Sx)
            value2 = exp(-self.div_rate * self.gap)
            value3 = (1 - value2 * self.__N__(self.__D1_Negtive__(Sx))) * Sx / self.q1
            y = (value1 - value3 + Sx - self.strike) ** 2
            return y

        return

    # 迭代模拟求解的最小值

    def __simulate_spot_star__(self):

        func = lambda s: self.__func_spot_star__(s)
        start = self.spot
        data = opt.fmin(func, start)
        self.spot_star = data[0]

        return

    def __D1_Postive__(self, S):

        temp = log(S / self.strike) + (self.rate - self.div_rate + 0.5 * self.volatility ** 2)
        temp = temp / self.volatility / sqrt(self.gap)

        return temp

    def __D1_Negtive__(self, S):

        temp = -log(S / self.strike) + (self.rate - self.div_rate + 0.5 * self.volatility ** 2)
        temp = temp / self.volatility / sqrt(self.gap)

        return temp

    def __A__(self):

        self.__q__()
        self.__simulate_spot_star__()

        if self.option_type == 'CALL':
            self.A1 = 0
            self.A2 = 1 - exp(-self.div_rate * self.gap)
            *self.__N__(self.__D1_Postive__(S=self.spot_star))
            self.A2 = self.A2 * (self.spot_star / self.q1)
            return

        if self.option_type == 'PUT':
            self.A1 = 1 - exp(-self.div_rate * self.gap)
            *self.__N__(self.__D1_Negtive__(S=self.spot_star))
            self.A1 = -self.A1 * (self.spot_star / self.q1)
            self.A2 = 0
            return


        print("期权类型错误")
        return

    def compute_American_call(self):
        self.option_type = "CALL"

        self.__A__()

        if self.spot >= self.spot_star:
            self.NPV = self.spot - self.strike
            print("NPV = %f" % self.NPV)
            return

        self.Euro_CALL_NPV = self.__Euro_call__(self.spot)

        self.NPV = self.Euro_CALL_NPV + self.A2*(self.spot / self.spot_star) ** self.q2

        return


    def compute_American_put(self):
        self.option_type = "PUT"

        self.__A__()

        if self.spot <= self.spot_star:
            self.NPV = self.strike - self.spot
            return

        self.Euro_PUT_NPV = self.__Euro_put__(self.spot)

        self.NPV = self.Euro_PUT_NPV + self.A1*(self.spot / self.spot_star) ** self.q1


    return

    pass
