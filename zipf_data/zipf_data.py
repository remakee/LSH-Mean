# -*- coding:utf-8 -*-
# import sys
# import os
import numpy as np
import random
# import math
from scipy import special
# import matplotlib.pyplot as plt


def Guass_data(dim, N, C, mean_size=10, cov_size=0.25):
    """
    :param dim: 生成数据集的维度
    :param N: 生成数据的数量
    :param C: 簇的个数
    :return: 服从高斯分布的 N × dim 维数组
    """
    def gen_mean():
        mean = [np.random.randint(-10, mean_size) for _ in range(dim)]
        return mean

    means = []
    for _ in range(C):
        mean = gen_mean()
        while mean in means:
            mean = gen_mean()
        means.append(mean)
    # means = [[np.random.randint(1, 1000) for _ in range(dim)] for _ in range(C)]
    covs = [[[np.random.randint(0, cov_size) if j == i else 0 for i in range(dim)] for j in range(dim)] for _ in range(C)]
    datas = []
    for mean, cov in zip(means, covs):
        datas.extend(np.random.multivariate_normal(mean, cov, N))
        # datas.append(np.random.multivariate_normal(mean, cov, N))

    return datas


def zipf_prob(r, a=1.5):
    """

    :param a: 约等于1
    :param r: 出现频率的排名
    :return: p(r): 排名为r的出现的频率
    """
    # x = np.arange(1, r)
    # print(special.zetac(a))
    p = r ** (-a) / special.zetac(a)
    return p


def zipf_data(datas, a=1.5):
    """

    :param datas: Guass_data
    :return:
    """
    zipf_datas = []
    for i in range(len(datas)):
        zipf_p = zipf_prob(i+1, a)
        # tmp = []
        for j in datas[i]:
            if random.uniform(0, 1) < zipf_p:
                # tmp.append(j)
                zipf_datas.append(j)

    return zipf_datas


# if __name__ == '__main__':
#     guass_data = Guass_data(2, 10000, 50)
#     # print(guass_data)
    # datas = np.array(zipf_data(guass_data, a=2))
    # np.save('test', datas)
    #
    # ldata = np.load('test.npy')
    # print(len(datas), len(ldata))
    # for i in datas:
    #     print(i）


