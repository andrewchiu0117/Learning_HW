import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
import random

def normalize(data): #正規劃
    min_max_scaler = preprocessing.MinMaxScaler()
    normalize = min_max_scaler.fit_transform(data)

    return normalize

def read_dataset():
    f = open("machine.data", "r")
    cnt = 0
    data = []

    for d in f:
        data.append([])
        dd = d[:len(d)-1].split(",", 10)
        for i in range(2, 9):
            data[cnt].append(int(dd[i]))
        cnt += 1

    f.close()
    return data
    

#分資料集 training set：test set = 7 : 3
def train_test_split(data):
    train_data = dict()
    train_label = dict()
    test_data = dict()
    test_label = dict()

    random.shuffle(data)

    train_cnt = 0
    test_cnt = 0

    for train_cnt in range(0, len(data)):
        if train_cnt < (len(data) * 0.7):
            train_data[train_cnt] = (data[train_cnt][0], data[train_cnt][1], data[train_cnt][2], data[train_cnt][3], data[train_cnt][4], data[train_cnt][5])
            train_label[train_cnt] = data[train_cnt][6]
        else:
            test_data[test_cnt] = (data[train_cnt][0], data[train_cnt][1], data[train_cnt][2], data[train_cnt][3], data[train_cnt][4], data[train_cnt][5])
            test_label[test_cnt] = data[train_cnt][6]
            test_cnt += 1

    
    return train_data, train_label, test_data, test_label

class Calc_result:
    def __init__(self, dist, label):
        self.dist = dist
        self.label = label
    
    def get_dist(self):
        return self.dist
    
    def get_label(self):
        return self.label


def euclidean_distance(x, y):
    import math
    if len(x) != len(y):
        return 0
    
    sum = 0
    for i in range(0, len(x)):
        sum += math.pow(math.fabs(float(x[i]) - float(y[i])), 2)

    return math.sqrt(sum)

#算所有test data的class
def knn_with_all(res, k = 3):
    predict = dict()

    for i in range(0, len(res)):
        predict[i] = knn_regression(res[i], k)

    return predict

def knn_regression(one_res, k):
    sum = 0.0
    if k > len(one_res):
        return 0

    for i in range(1, k):
        sum += float(one_res[i].get_label())
    
    return sum/k

def sort_cmp(elem):
    return elem.get_dist()

#使用均方根誤差來判斷Knn regression的結果好壞
def root_mean_square_error(expect, actual):
    import math
    error = []

    for i in range(0, len(expect)):
        error.append(float(expect[i]) - float(actual[i]))
  
    squaredError = []
    for var in error:
        squaredError.append(math.pow(var, 2))

    return math.sqrt(sum(squaredError) / len(squaredError))

def knn_execute(dataset):
    train_data, train_label, test_data, test_label = train_test_split(dataset)
    res = []

    #計算所有測資的距離
    for i in range(0, len(test_data)):
        tmp = []
        for j in range(len(train_data)):
            dist = euclidean_distance(test_data[i], train_data[j])
            tmp.append(Calc_result(dist, train_label[j]))
        
        res.append(tmp)

    #排序計算後距離
    for i in range(0, len(test_data)):
        res[i].sort(key=sort_cmp)

    rmse_array = []
    #計算結果k = 3 ~ 15
    for i in range(3, 16):
        predict = knn_with_all(res, i)
        rmse = root_mean_square_error(predict, test_label)
        rmse_array.append(rmse)

    return rmse_array

def main():
    data = read_dataset()
    dataset=normalize(data)
    rmse = []
    rmse_array = []

    for i in range(0, 13):
        rmse_array.append(0.0)

    for i in range(0, 10):
        rmse.append(knn_execute(dataset))
        for j in range(0, len(rmse[i])):
            rmse_array[j] += rmse[i][j]

    for i in range(3, 16):
        print("k =", i, ", RMSD = ", end='')
        rmse_array[i-3] = rmse_array[i-3]/10
        print(rmse_array[i-3])

    #draw
    plt.plot(range(3, 16), rmse_array)
    plt.show()

if __name__ == '__main__':
    main()