from sklearn.neighbors import KNeighborsRegressor
import numpy as np
def read_data():
    f = open("machine.data", "r")
    data = []
    for line in f:
        dd = line[:len(line)-1].split(",", 11)
        count = int(dd[8])
        data.append(count)
    f.close()
    return data



def main():
    data=read_data()
    #print(data)

    '''uni_knr=KNeighborsRegressor(weights='uniform')   #初始化平均回归的KNN回归器
    uni_knr.fit(X_train,y_train)
    uni_knr_y_predict=uni_knr.predict(X_test)

    dis_knr=KNeighborsRegressor(weights='distance')   #初始化距离加权回归的KNN回归器
    dis_knr.fit(X_train,y_train)
    dis_knr_y_predict=dis_knr.predict(X_test)'''


if __name__ == "__main__":
    main()