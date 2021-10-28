# -*- coding:utf-8 -*-
from hash_01 import *
from sklearn.cluster import KMeans
import os
import math
import time


src_path = ".//rawdataset"

save_path = ".//newdataset"
if not os.path.exists(save_path):
    os.mkdir(save_path)

for file_name in os.listdir(src_path):
    if file_name[-4:] == ".npy":
        print(file_name)
        data = np.load(os.path.join(src_path, file_name))
        data = np.asarray(data)

        print(data.shape)

        K = range(2, 100)
        L = []
        for no, k in enumerate(K, 1):
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(data)

            L.append((k, kmeans.inertia_))

        n, dim = data.shape
        E2LSH = lsh(vecsize=dim, dataName=file_name[:-4])
        E2LSH.lshash(data)
        sample_factor = [0.1, 0.2, 0.25]
        # sample_factor = [0.1, 0.2, 0.25]
        time_start = time.time()
        LSH_SSE = []
        print(E2LSH.bucket_num())
        for i in sample_factor:
            all_data = []
            sample_bucket_num = math.floor(E2LSH.bucket_num() * i)
            each_bucket_data = E2LSH.get_bucket_data(sample_bucket_num)

            for bucket_data in each_bucket_data:
                all_data.extend(bucket_data)
            all_data = np.asarray(all_data)

            print(all_data.shape)

            M = []
            for no, k in enumerate(K, 1):
                kmeans = KMeans(n_clusters=k)
                kmeans.fit(all_data)
                M.append((k, kmeans.inertia_))

            LSH_SSE.append(M)
            time_end = time.time()
            dtime = time_end - time_start

            print("程序运行时间: %d s" % dtime)

        for temp in LSH_SSE:
            if not len(temp) == len(L):
                print("len is not equal exit")
                exit()

        temp = [0 for _ in range(1 + len(LSH_SSE))]
        with open(".//{}//{}SSE.txt".format(save_path, file_name[:-4]), "w", encoding="UTF-8") as saveFile:
            with open(".//{}//{}SSE_ratio.txt".format(save_path, file_name[:-4]), "w", encoding="UTF-8") as saveFile2:

                for no in range(len(L)):
                    line_loss = ""
                    line_ratio = ""
                    K1, loss1 = L[no]
                    line_loss += "{} {}".format(K1, loss1)
                    index = 1
                    if no > 1:
                        line_ratio += "{} {}".format(K1, temp[0] / loss1)
                    temp[0] = loss1

                    for rol in range(len(LSH_SSE)):
                        K2, loss2 = LSH_SSE[rol][no]
                        index += 1
                        if K1 == K2:
                            line_loss += " {}".format(loss2)  # K value, K-means SSE , LSH SSE
                            if no > 1:
                                line_ratio += " {}".format(temp[rol + 1] / loss2)
                            temp[rol + 1] = loss2
                        else:
                            print("K is error")
                            print(K1, K2)

                    saveFile.write(line_loss + "\n")
                    if no > 1:
                        saveFile2.write(line_ratio + "\n")

        # dst_path = os.path.join(save_path, file_name[-5:])
        print("\n\n\n")


