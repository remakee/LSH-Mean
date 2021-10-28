import numpy as np
import os


class lsh:
    def __init__(self, vecsize, dataName, mu=0.0, sig=0.25, l=10, L=1, buckets=10, path="..//dataset"):
        """
        :param vecsize:  输入数据维度
        :param mu:  均值
        :param sig:  方差
        :param l:   signature由多少个哈希函数构成
        :param L:   哈希表的个数
        :param buckets:  限定每个哈希表的数量（暂时废弃）
        """
        version = "_mu={}_sig={}_l={}".format(mu, sig, l)
        a_save_path = "{}{}A{}.npy".format(path, dataName, version)
        b_save_path = "{}{}B{}.npy".format(path, dataName, version)
        # r_save_path = "{}{}R{}.npy".format(path, dataName, version)
        a_load_path = "{}{}A{}.npy".format(path, dataName, version)
        b_load_path = "{}{}B{}.npy".format(path, dataName, version)
        r_load_path = "{}{}R{}.npy".format(path, dataName, version)
        if os.path.exists(a_load_path) and os.path.exists(b_load_path) and os.path.exists(r_load_path):
            self.a = np.load(a_load_path)
            self.b = np.load(b_load_path)
        else:

            self.a = np.asarray([np.random.normal(mu, sig, vecsize) for _ in range(l)])
            self.b = np.asarray([np.random.uniform(0, 10) for _ in range(l)])

            np.save(a_save_path, self.a)
            np.save(b_save_path, self.b)

        self.h = [dict() for _ in range(L)]

    def lshash(self, vec, table_index=0):
        """
        暂时没有进行二次哈希，查找速度较慢
        :param vec:  输入的值
        :return:
        """
        index_Matrix = np.floor((vec.dot(self.a.transpose()) + self.b))
        for index, signature in enumerate(index_Matrix):
            sig = str(signature.tolist())
            if sig in self.h[table_index]:
                self.h[table_index][sig].append(vec[index])  # 放的是原始数据，比较浪费内存
            else:
                self.h[table_index][sig] = [vec[index]]

    def __setitem__(self, vec, value, idx=0):
        """
        :param idx: 哈希表的序号（即取第几个哈希表）
        :param vec: 【输入的原始向量】
        :param value: 哈希值
        :return:
        """
        self.h[idx][value] = vec

    def __getitem__(self, value, idx=0):
        return self.h[idx][value]

    def bucket_num(self, idx=0):
        bucket = self.h[idx]
        bukcet_key_list = bucket.keys()
        return len(bukcet_key_list)

    def bucket_show(self, idx=0):
        no = 0
        for key in self.h[idx]:
            print("bukcet{} information:".format(no + 1))
            print("signature:", key)
            print("bucket data:")
            for data in self.h[idx][key]:
                print(data)
            print()
            no += 1

    def get_bucket_data(self, bucket_num, idx=0):
        bucket_data_Matrix = []
        count = 0
        for key in self.h[idx]:
            bucket_data_Matrix.append(np.asarray(self.h[idx][key]))
            count += 1
            if count >= bucket_num:
                break
        print(len(bucket_data_Matrix))

        return bucket_data_Matrix

