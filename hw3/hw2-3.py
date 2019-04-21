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
        if line <  (len(data) * 0.3):
            data_test.append(data[line])
        else :
            data_train.append(data[line])
            
    return data_test,data_train

def count_probablity(data_train): #計算機率表
    data=numpy.array(data_train)
    label_count=[]
    benign_count=[]
    for attribute in range(0,9):
        label_count.append([0,0,0,0,0,0,0,0,0,0])
        benign_count.append([0,0,0,0,0,0,0,0,0,0])
    for line in data:
        for attribute in range(0,9):
            for count in range(0,10):
                if line[attribute]==(count+1):
                    if line[9]==2:
                        benign_count[attribute][count]+=1
                    label_count[attribute][count]+=1
                    break
    return label_count,benign_count

def judge(x,y):
    if x==y:
        return True
    else:
        return False
    
def accuracy(data_test,label_count,benign_count):
    correct=0
    for line in data_test:
        guess=2
        accuracy_benign=1
        accuracy_malignant=1
        for attribute in range(0,9):
            if label_count[attribute][line[attribute]-1]!=0:
                accuracy_benign*=benign_count[attribute][line[attribute]-1]/label_count[attribute][line[attribute]-1]
                accuracy_malignant*=1-(benign_count[attribute][line[attribute]-1]/label_count[attribute][line[attribute]-1])
        if accuracy_benign > accuracy_malignant:
            guess=2
        else:
            guess=4
        
        if(judge(guess,line[9])):
            correct+=1
    return correct/len(data_test)

def run_times(times):
    data=read_data()
    answers=[]
    temp=0
    for x in range(times):
        data_test,data_train=shuffle_split(data)
        label_count,benign_count=count_probablity(data_train)
        answer=accuracy(data_test,label_count,benign_count)
        answers.append(answer)
    import matplotlib.pyplot as plt
    time_label=[1,2,3,4,5,6,7,8,9,10]
    for x in range(times):
        temp+=answers[x]
    temp/=10
    print("Total accuracy:",temp)
    plt.plot(time_label,answers)
    plt.show()

def main():
    run_times(10)
    

if __name__ == "__main__":
    main()