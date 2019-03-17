import random
import numpy
import matplotlib.pyplot as plt
#import numba as nb 
#from numba import jit 


def takeSecond(elem):
    return elem[1]

def cleanQuestionData(f):
    text = []
    for line in f:
        checked=0
        check=line.split(',')
        for i in range (0,10):
            if check[i]=='?':
                checked=1
                break
        if checked==0:
            text.append(check)

    return text

def main():
    f = open(r'breast-cancer-wisconsin.data.txt')
    text=cleanQuestionData(f)

    accuracy_out=[]
    for times in range(10):
        print("Times=",times)
        text_K=text        
        random.shuffle(text_K)
        accuracy_out.append([])
        for K in range (3,16):
            correct_count=0
            for test_item in range (0,204): #205個test data
                training_num=[]
                for compare_item in range (0,477): #比較478個training data
                    sum=0
                    for j in range (1,9): #1~9的參數
                        sum=sum+numpy.square(int(text_K[205+compare_item][j]) - int(text_K[test_item][j]))
                    distance=numpy.sqrt(sum)
                    tuples=205+compare_item  , distance
                    training_num.append(tuples)
                training_num.sort(key=takeSecond,reverse = False)

                count=0
                for j in range (K):
                    if text_K[ training_num[j][0] ][10] == "2\n":
                        count=count+1
                Ans=int(text_K[test_item][10])
                if count > (K/2):
                    real=2
                else:
                    real=4
                if Ans==real:
                    correct_count=correct_count+1
            #print("Times=",times,",K=",K,",accuracy=",correct_count/205)
            accuracy_out[times].append(correct_count/205)

    final_accuracy=[]
    K_out=[]
    total_accuracy=0
    for k in range(13):
        average=0
        for t in range(10):
            average=average+accuracy_out[t][k]
        average=average/10
        print("Average accuracy: K=",k+3,",accuracy=",average)
        final_accuracy.append(average)
        K_out.append(k+3)
    for t in range(10):
        total_accuracy=total_accuracy+final_accuracy[t]
    total_accuracy=total_accuracy/10
    print("Total accuracy=",total_accuracy)

    plt.plot(K_out,final_accuracy)
    plt.show()

if __name__ == "__main__":
    main()