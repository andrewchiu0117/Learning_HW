import numpy as np
def read_data(): #讀資料
    f = open("breast-cancer-wisconsin.data", "r")
    count = 0
    data = dict()
    for line in f:
        if line.find('?') == -1:
            dd = line[:len(line)-1].split(",", 11)
            data[count] = (int(dd[1]), int(dd[2]), int(dd[3]), int(dd[4]), int(dd[5]), int(dd[6]), int(dd[7]), int(dd[8]), int(dd[9]))
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


def normalize(data_test,data_train):
    from sklearn.preprocessing import StandardScaler
    stdsc = StandardScaler()
    data_train_std = stdsc.fit_transform(data_train)
    data_test_std = stdsc.fit_transform(data_test)
    return data_test_std,data_train_std

def eigen(cov_mat):
    #求共變異係數矩陣 的特徵向量及特徵值
    eigen_vals, eigen_vecs = np.linalg.eig(cov_mat)
    # print("特徵向量.shape=",eigen_vecs.shape)
    # print("特徵向量=",eigen_vecs)
    # print("特徵值=",eigen_vals)
    return eigen_vals, eigen_vecs

def print_graph(eigen_vals):

    #計算解釋變異數比率 各特徵值/特徵值總和
    tot = sum(eigen_vals)
    var_exp = [(i / tot) for i in sorted(eigen_vals, reverse=True)]
    cum_var_exp = np.cumsum(var_exp)
    print("各特徵值變異數比率：",var_exp)
    print("特徵值變異數比率累加：",cum_var_exp)


    import matplotlib.pyplot as plt
    #畫圖 ：解釋變異數比率 ，各特徵值/特徵值總和
    plt.bar(range(1, 10), var_exp, alpha=0.5, align='center',label='PoV(k)')
    plt.step(range(1, 10), cum_var_exp, where='mid',label='cumulative PoV(k)')
    plt.ylabel('Explained variance ratio')
    plt.xlabel('k')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()

def Covariance_matrix(data_train_std): #求共變異係數矩陣
    cov_mat = np.cov(data_train_std.T)
    # print("共變異係數矩陣.shape=",cov_mat.shape)
    # print("共變異係數矩陣=",cov_mat)
    return cov_mat

def main():
    data=read_data()
    data_test,data_train=shuffle_split(data)
    data_test_std,data_train_std=normalize(data_test,data_train)
    cov_mat=Covariance_matrix(data_train_std)
    eigen_vals, eigen_vecs=eigen(cov_mat)
    print_graph(eigen_vals)
    

if __name__ == "__main__":
    main()