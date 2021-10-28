# -*- coding:utf-8 -*-
import numpy as np


def Guass_data(dim, N, C, mean_size=20, cov_size=0.25):
    """
    :param dim: 生成数据集的维度
    :param N: 生成数据的数量
    :param C: 簇的个数
    :return: 服从高斯分布的 N × dim 维数组
    """
    def gen_mean():
        mean = [np.random.randint(-30, mean_size) for _ in range(dim)]
        return mean

    means = []
    for _ in range(C):
        mean = gen_mean()
        while mean in means:
            mean = gen_mean()
        means.append(mean)
    # means = [[np.random.randint(1, 1000) for _ in range(dim)] for _ in range(C)]

    covs = [[[np.random.randint(0, cov_size) if j == i else 0 for i in range(dim)] for j in range(dim)] for _ in range(C)]

    # covs = [[[np.random.randint(1, cov_size) if j == i else 0 for i in range(dim)] for j in range(dim)] for _ in
    # range(C)]
    datas = []
    for mean, cov in zip(means, covs):
        # datas.extend(np.random.multivariate_normal(mean, cov, N))
        datas.append(np.random.multivariate_normal(mean, cov, N))
    return datas




