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
    random.shuffle(data)
    for line in range(0, len(data)):
        if line <  205:
            data_test.append(data[line])
        else :
            data_train.append(data[line])
            
    return data_test,data_train


def euclidean_distance(m1, m2): #算距離
    v1=numpy.array(m1)
    v2=numpy.array(m2)
    distance = numpy.linalg.norm(v1 - v2)
    return distance

def takeSecond(elem): #去第二位
    return elem[1]

def final_print(K_array): #print
    import matplotlib.pyplot as plt
    print(K_array)
    K_out=[3,4,5,6,7,8,9,10,11,12,13,14,15]
    total_accuracy=0
    for k in range(13):
        K_array[k]/=2050
        total_accuracy+=K_array[k]
        print("K=",k+3,",accuracy=",K_array[k])
    total_accuracy/=13
    print("Total accuracy=",total_accuracy)

    plt.plot(K_out,K_array)
    plt.show()

def main():
    data=read_data()
    K_array=[0,0,0,0,0,0,0,0,0,0,0,0,0]
    for times in range(10):
        print("Times=",times)
        data_test,data_train=shuffle_split(data)    
        for test_item in range (0,205): #205個test data
            training_num=[]
            for compare_item in range (0,478): #比較478個training data
                distance=euclidean_distance(data_train[compare_item],data_test[test_item])

                tuples = compare_item , distance
                training_num.append(tuples)
            training_num.sort(key=takeSecond,reverse = False) #排名
            for K in range (3,16):
                count=0
                for j in range (K):
                    if data_train[ training_num[j][0] ][9] == 2: #計算為2的次數
                        count=count+1
                
                if count > (K/2): #vote for 2
                    real=2
                else:
                    real=4

                if data_test[test_item][9]==real:
                    K_array[(K-3)]+=1
    final_print(K_array)

    

if __name__ == "__main__":
    main()