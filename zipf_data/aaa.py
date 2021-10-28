# -*- coding:utf-8 -*-
from scipy import special
import numpy as np
import random


def zipf_prob(r, a=2.0):
    """
    一个单词出现的频率与它在频率表里的排名成反比
    :param a: 约等于1
    :param r: 出现频率的排名
    :return: p(r): 排名为r的出现的频率
    """
    x = np.arange(1, r)
    # print(special.zetac(a))
    p = x ** (-a) / special.zetac(a)
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
    pr = zipf_prob(50, 1.5)
    a = 0
    for i in pr:
        a += i

    print(a)

    print("概率", pr, len(pr))


