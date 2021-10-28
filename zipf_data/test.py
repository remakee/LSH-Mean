# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
import numpy as np
import random
from scipy import special


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

    covs = [[[0.25 if j == i else 0 for i in range(dim)] for j in range(dim)] for _ in range(C)]

    # covs = [[[np.random.randint(1, cov_size) if j == i else 0 for i in range(dim)] for j in range(dim)] for _ in
    # range(C)]

    datas = []
    for mean, cov in zip(means, covs):
        # datas.extend(np.random.multivariate_normal(mean, cov, N))
        datas.append(np.random.multivariate_normal(mean, cov, N))
    return datas


def zipf_prob(r, a=2.0):
    """
    一个单词出现的频率与它在频率表里的排名成反比
    :param a: 约等于1
    :param r: 出现频率的排名
    :return: p(r): 排名为r的出现的频率
    """
    # x = np.arange(1, r)
    # print(special.zetac(a))
    p = r ** (-a) / special.zetac(a)
    print('try:', p)
    return p


def zipf_data(datas, a=1.5):
    """

    :param datas: Guass_data
    :return:
    """
    zipf_datas = []
    for i in range(len(datas)):
        zipf_p = zipf_prob(i+1, a)
        tmp = []
        for j in datas[i]:
            if random.uniform(0, 1) < zipf_p:
                tmp.append(j)
                zipf_datas.append(j)

    return zipf_datas


if __name__ == '__main__':
    guass_data = Guass_data(dim=10, N=100000, C=50)
    data = np.asarray(guass_data)
    print(data.shape)
    ldata = np.asarray(zipf_data(data, a=1.5))
    print(ldata.shape)
    np.save('test_data', ldata)






