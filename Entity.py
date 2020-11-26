import matplotlib as matplotlib
import numpy as np
import warnings
import pandas as pd
import scipy.stats as st
import statsmodels as sm
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
matplotlib.style.use('ggplot')
# Create models from data
def best_fit_distribution(data, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Distributions to check
    DISTRIBUTIONS = [
        st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
        st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
        st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
        st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
        st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
        st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
        st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
        st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
        st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
        st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
    ]

    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                    # end
                except Exception:
                    pass

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (best_distribution.name, best_params)

def reach_the_exit(entity , exit):
    if exit[0]==15:
        if (entity.r[0] <= exit[0]) or (entity.r[1] < exit[1] - 0.5) or (entity.r[1] > exit[1] + 0.5):
            return False
    else:
        if (entity.r[0] >= exit[0]) or (entity.r[1] < exit[1] - 0.5) or (entity.r[1] > exit[1] + 0.5):
            return False
    return True



#####################################################################################################
#1
R_k_matrix=[]
class Entity:
    def __init__(self, r):
        self.e = [0,0]
        self.v = [0,0]
        self.prev_v = [0, 0]
        self.r = r
        self.v0 = 1.5
        self.acceleration_time = 0.5

    def update_e(self, exit):
        size = ((exit[0]-self.r[0])**2+(exit[1]-self.r[1])**2)**0.5
        self.e = [(exit[0]-self.r[0])/size, (exit[1]-self.r[1])/size]

    def update_v(self):
         self.v = [self.v[0]+(self.v0*self.e[0]-self.v[0])*0.01/self.acceleration_time, self.v[1]+(self.v0*self.e[1]-self.v[1])*0.01/self.acceleration_time]
        # temp_v=(self.v[0],self.v[1])
        # self.v=(self.v[0]+(self.v[0]-self.prev_v[0])/0.01 , self.v[1]+(self.v[1]-self.prev_v[1])/0.01)
        # self.prev_v = temp_v

    def update_r(self):
        self.r = [self.r[0]+self.v[0]*0.01, self.r[1]+self.v[1]*0.01]


def simulate_one_entity(entity, exit):
    k=0
    v = []
    r = []
    plot_x = []
    plot_y = []
    plot_x_v = []
    plot_y_v = []
    k_array=[]
    entity.update_e(exit)
    while not reach_the_exit(entity, exit):
        v.append(entity.v)
        r.append(entity.r)
        k_array.append(k)
        plot_x.append(entity.r[0])
        plot_y.append(entity.r[1])
        plot_x_v.append(entity.v[0])
        plot_y_v.append(entity.v[1])
        entity.update_v()
        entity.update_r()
        k = k + 1
    v.append(entity.v)
    r.append(entity.r)
    print("my k is:"+str(k))
    # result=set(zip(k_array,r))
    # for i in result:
    #     if i in dict:
    #         dict[i]=dict[i]+1
    #     else:
    #         dist=i[1]
    #         if i[0]
    #         dict[i]=1
    R_k_matrix.append(r)
    print(v)
    # print(r)
    return k,plot_x,plot_y,k_array,plot_x_v,plot_y_v,R_k_matrix
# # #A
# exit = [15,15/2]
# entity = Entity([15/2, 15/2])
# k,plot_x,plot_y,k_array,plot_x_v,plot_y_v = simulate_one_entity(entity, exit)
# print("time:"+str(k))

#
#
#
# import matplotlib.pyplot as plt
#
# # x axis values
# x1 = plot_x
# # corresponding y axis values
# y1 = plot_y
# # plotting the points
# plt.plot(x1, y1)
# # naming the x axis
# plt.xlabel('x - location')
# # naming the y axis
# plt.ylabel('y - location')
#
# # giving a title to my graph
# plt.title('question A - 1')
#
# # function to show the plot
# plt.show()
#
# # x axis values
# x2 = k_array
# # corresponding y axis values
# y2 = plot_x_v
# # plotting the points
# plt.plot(x2, y2)
# # naming the x axis
# plt.xlabel('x - time')
# # naming the y axis
# plt.ylabel('y - velocity(x axis)')
#
# # giving a title to my graph
# plt.title('question A - 2')
#
# # function to show the plot
# plt.show()


# c
def getCol(R_K_matrix):
    counterCol = 0

    for i in range(len(R_K_matrix)):
        j = i + 1
        for j in range(len(R_K_matrix)):
            array_i = R_k_matrix[i]
            array_j = R_k_matrix[j]
            min_len_array = min(len(array_i), len(array_j))
            k = 0

            while k < min_len_array:
                if abs(array_i[k][0] - array_j[k][0]) <= 0.5 or abs(array_i[k][1] - array_j[k][1]) <= 0.5:
                    counterCol = counterCol + 1
                k = k + 1
                print(str(k))

    return counterCol

#B
dict={}
np.random.seed(0)
random0 = np.random.uniform(0,15,200)
np.random.seed(2)
random1 = np.random.uniform(0,15,200)
k_array = []
exit = [15,15/2]
for i in range(200):
    entity = Entity([random0[i],random1[i]])
    k, plot_x, plot_y, k_array_from_fun, plot_x_v, plot_y_v,R_k_matrix=simulate_one_entity(entity,exit)
    # print("apennded k:"+str(k))
    k_array.append(k)

print("total collision" + str(getCol(R_k_matrix)))
# print(k_array)
# print(max(k_array))
# print(best_fit_distribution(k_array))







#######################################################################################################
