import numpy
def read_data(): #讀資料
    f = open("breast-cancer-wisconsin.data", "r")
    count = 0
    data = dict()
    for line in f:
        if line.find('?') == -1:
            dd = line[:len(line)-1].split(",", 11)
            data[count] = (int(dd[1]), int(dd[2]), int(dd[3]), int(dd[4]), int(dd[5]), int(dd[6]), int(dd[7]), int(dd[8]), int(dd[9]), int(dd[10]))
            count += 1
    f.close()
    return data
    
def shuffle_split(data): #random後分裂
    import random
    data_test=[]
    data_train=[]
    data_find=[]
    random.shuffle(data)
    for line in range(0, len(data)):
        if line <  (len(data) * 0.3):
            data_test.append(data[line])
        elif line <  (len(data) * 0.5) and line >=  (len(data) * 0.3):
            data_find.append(data[line])
        else :
            data_train.append(data[line])
            
    return data_test,data_find,data_train


def euclidean_distance(m1, m2,attributes): #算距離
    import math
    answer=0
    for x in range(0,3):
        answer+=math.pow(m1[attributes[x]]-m2[attributes[x]],2)
    distance=math.pow(answer,0.5)
    return distance

def takeSecond(elem): #去第二位
    return elem[1]

def compare_train(attribute,item,data_train):
    benign_count=0
    malignant_count=0
    for line in data_train:
        if line[attribute]==item:
            if line[9]==2:
                benign_count+=1
            else:
                malignant_count+=1
    if benign_count >= malignant_count:
        return 2
    else:
        return 4


def knn_best_attribute(data_find,data_train):
    correct_attribute=[]
    for x in range(0,9):
        tuples=[x,0]
        correct_attribute.append(tuples)
    for line in data_find:
        for attribute in range(0,9):
            if line[9]==compare_train(attribute,line[attribute],data_train):
                correct_attribute[attribute][1]+=1
    correct_attribute.sort(key=takeSecond,reverse=True)
    #print(correct_attribute)
    attributes=[correct_attribute[0][0],correct_attribute[1][0],correct_attribute[2][0]]
    return attributes

def compare_train_3(test,data_train,attributes):
    training_num=[]
    for train in data_train:
        distance=euclidean_distance(test,train,attributes)
        training_num.append([train,distance])
    training_num.sort(key=takeSecond,reverse = False) #排名
    result=vote(training_num)
    if test[9]==result:
        return True
    else:
        return False

def vote(training_num):
    count=0
    K=3
    for j in range (K):
        if training_num[j][0][9]== 2: #計算為2的次數
            count=count+1
    
    if count > (K/2): #vote for 2
        return 2
    else:
        return 4

def knn_3_test(data_test,data_train,attributes):
    correct_times=0
    for test in data_test:
        if (compare_train_3(test,data_train,attributes)):
            correct_times+=1
    return (correct_times/len(data_test))

def print_graph(answer):
    import matplotlib.pyplot as plt
    x=[1,2,3,4,5,6,7,8,9,10]
    plt.plot(x,answer)
    plt.show()
            
def run_times(times):
    data=read_data()
    answer=[]
    temp=0
    for x in range(times):
        data_test,data_find,data_train=shuffle_split(data)
        attributes=knn_best_attribute(data_find,data_train)
        #print("Selected attributes:" ,attributes)
        answer.append(knn_3_test(data_test,data_train,attributes))

    for x in range(times):
        temp+=answer[x]
    temp/=10
    print("Total accuracy:",temp)

    print_graph(answer)


def main():
    run_times(10)

if __name__ == "__main__":
    main()