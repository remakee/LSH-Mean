# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
import numpy as np
from sklearn.cluster import KMeans
import os
import time

# src_path = "../sampledata"
src_path = "./rawdataset"
save_path = "./newdataset"

for file_name in os.listdir(src_path):
    if not file_name == "avila.npy":
        continue
    print(file_name)
    data = np.load(os.path.join(src_path, file_name))
    data = np.asarray(data)

    X = data

    res = []
    left = 2
    right = 100

    kmeans1 = KMeans(n_clusters=left)
    kmeans1.fit(X)
    left_loss = kmeans1.inertia_
    res.append([left, left_loss])

    kmeans2 = KMeans(n_clusters=right)
    kmeans2.fit(X)
    right_loss = kmeans2.inertia_
    res.append([right, right_loss])
    # print("right left over")
    while left < right - 1:
        time_start = time.time()
        mid = int((left + right) / 2)
        kmeans3 = KMeans(n_clusters=mid)
        kmeans3.fit(X)
        mid_loss = kmeans3.inertia_
        res.append([mid, mid_loss])

        left_ratio = left_loss / mid_loss
        right_ratio = mid_loss / right_loss
        if left_ratio > right_ratio:
            right = mid
            right_loss = mid_loss
        else:
            left = mid
            left_loss = mid_loss
        time_end = time.time()
        dtime = time_end - time_start
        print("程序%d %d运行一次二分时间：%d s" % (left, right, dtime))
        # mid_loss = KMeans(n_clusters=mid, init="k-means++", n_init=10, max_iter=300, tol=1e-04,
        #                   random_state=10).inertia_
        # leaf_ratio = left_loss / mid_loss
        # right_ratio = mid_loss / right_loss

    with open(".//{}//{}k_loss_tuple.txt".format(save_path, file_name), "w") as f:
        for k, loss in res:
            f.write("{} {}\n".format(k, loss))


