import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
import random
import math

def normalize(data): #normalize
    min_max_scaler = preprocessing.MinMaxScaler()
    normalize = min_max_scaler.fit_transform(data)
    return normalize

def read_data():
    f = open("machine.data", "r")
    count = 0
    data = []

    for line in f:
        data.append([])
        para = line[:len(line)-1].split(",", 10)
        for i in range(2, 9):
            data[count].append(int(para[i]))
        count += 1

    f.close()
    return data

def random_split(data):
    train_y = []
    train_x = []
    test_y = []
    test_x = []

    random.shuffle(data)  #shuffle the data

    train_count = 0
    test_count = 0

    for train_count in range(0, len(data)):
        if train_count < (len(data) * 0.3):
            count=(data[train_count][0], data[train_count][1], data[train_count][2], data[train_count][3], data[train_count][4], data[train_count][5])
            test_x.append(count)
            test_y.append(data[train_count][6])
            test_count += 1
        else:
            count=(data[train_count][0], data[train_count][1], data[train_count][2], data[train_count][3], data[train_count][4], data[train_count][5])
            train_x.append(count)
            train_y.append(data[train_count][6])

    
    return test_x, test_y,train_x, train_y

def euclidean_distance(x, y):
    v1=np.array(x)
    v2=np.array(y)
    distance = np.linalg.norm(v1 - v2)
    return distance


def mean_square_error(expect, actual):
    return math.pow(float(expect - actual),2)

def takeSecond(elem): #去第二位
    return elem[1]

def knn_regression(training_num, k):
    sum = 0.0
    for i in range(k):
        sum += training_num[i][0]
    return sum/k

def knn(dataset):
    test_x, test_y,train_x, train_y = random_split(dataset)
    calcu=[]
    for i in range(13):
        calcu.append(0.0)

    #計算所有測資的距離
    for i in range(len(test_x)):
        training_num=[]
        for j in range(len(train_x)):
            distance = euclidean_distance(test_x[i], train_x[j])
            tuples =train_y[j],distance
            training_num.append(tuples)
        training_num.sort(key=takeSecond,reverse = False) #排名
        # print(training_num)
        for K in range (3,16):
            test_z = knn_regression(training_num,K)
            error=mean_square_error(test_z,test_y[i])
            calcu[K-3]+=error
    print(np.round(calcu,2))
    for i in range(13):
        calcu[i]/=len(test_x)
        calcu[i]=math.sqrt(calcu[i])
    return calcu            
            


def main():
    times=10
    rmse = []
    rmse_array = []
    data = read_data()

    for i in range(0, 13):
        rmse_array.append(0.0)

    for i in range(times):
        dataset=normalize(data)
        rmse.append(knn(dataset))
        for k in range(len(rmse[i])):
            rmse_array[k] += rmse[i][k]

    for i in range(3, 16): #print
        print("k =", i, ", RMSD = ", end='')
        rmse_array[i-3] = rmse_array[i-3]/times
        print(rmse_array[i-3])

    #draw
    plt.plot(range(3, 16), rmse_array)
    plt.show()

if __name__ == '__main__':
    main()