import numpy as np
def read_data(): #讀資料
    f = open("breast-cancer-wisconsin.data", "r")
    count = 0
    data = dict()
    for line in f:
        if line.find('?') == -1:
            dd = line[:len(line)-1].split(",", 11)
            data[count] = [int(dd[1]), int(dd[2]), int(dd[3]), int(dd[4]), int(dd[5]), int(dd[6]), int(dd[7]), int(dd[8]), int(dd[9]),int(dd[10])]
            count += 1
    f.close()
    return data

def shuffle_split(data): #random後分裂
    import random
    data_test=[]
    data_train=[]
    ans_test=[]
    ans_train=[]
    random.shuffle(data)
    for line in range(0, len(data)):
        if line <  (len(data) * 0.3):
            data_test.append(data[line][0:8])
            ans_test.append(data[line][9])
        else :
            data_train.append(data[line][0:8])
            ans_train.append(data[line][9])
            
    return data_test,data_train,ans_test,ans_train


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
    plt.bar(range(1, 9), var_exp, alpha=0.5, align='center',label='PoV(k)')
    plt.step(range(1, 9), cum_var_exp, where='mid',label='cumulative PoV(k)')
    plt.title("graph1")
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

def project_matrix(eigen_vals, eigen_vecs):
        # Make a list of (eigenvalue, eigenvector) tuples
    eigen_pairs = [(np.abs(eigen_vals[i]), eigen_vecs[:, i])
                for i in range(len(eigen_vals))]
    print("特徵值，特徵向量length：",len(eigen_pairs))
    print("特徵值，特徵向量：",eigen_pairs)
    # Sort the (eigenvalue, eigenvector) tuples from high to low
    eigen_pairs.sort(key=lambda k: k[0], reverse=True)
    print("特徵值，特徵向量排序：",eigen_pairs.sort(key=lambda k: k[0], reverse=True))
    #保留兩個最具影響力的特徵向量組成13x2 的投影矩陣W
    w = np.hstack((eigen_pairs[0][1][:, np.newaxis],
                eigen_pairs[1][1][:, np.newaxis]))
    print('Matrix W:\n', w)
    return w

def print_graph2(data_train_std,w,ans_train):
    import matplotlib.pyplot as plt
    #畫出轉換後的數據集 散點圖
    # print("data_train_std[0].dot(w)=",data_train_std[0].dot(w))
    X_train_pca = data_train_std.dot(w)
    colors = ['r', 'b', 'g']
    markers = ['s', 'x', 'o']
    for l, c, m in zip(np.unique(ans_train), colors, markers):
        plt.scatter(X_train_pca[ans_train == l, 0], 
                    X_train_pca[ans_train == l, 1], 
                    c=c, label=l, marker=m)
    plt.title("graph2")
    plt.xlabel('PC 1')
    plt.ylabel('PC 2')
    plt.legend(loc='lower left')
    plt.tight_layout()
    plt.show()

    return X_train_pca
    
def plot_decision_regions(X, y, classifier, resolution=0.02):##劃出決策分布圖
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    # setup marker generator and color map
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])
    # plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                        np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())
    # plot class samples
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1],
                    alpha=0.8, c=cmap(idx),
                    marker=markers[idx], label=cl)

def print_graph3(X_train_pca,ans_train):
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LogisticRegression#使用LogisticRegression 並用兩個PCA 主成分做訓練分類
    lr = LogisticRegression()
    lr = lr.fit(X_train_pca, ans_train)
    plot_decision_regions(X_train_pca, ans_train, classifier=lr)
    plt.title("graph3")
    plt.xlabel('PC 1')
    plt.ylabel('PC 2')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.show()

def main():
    data=read_data()
    data_test,data_train,ans_test,ans_train=shuffle_split(data)
    data_test_std,data_train_std=normalize(data_test,data_train)
    cov_mat=Covariance_matrix(data_train_std)
    eigen_vals, eigen_vecs=eigen(cov_mat)
    print_graph(eigen_vals)
    w=project_matrix(eigen_vals, eigen_vecs)
    X_train_pca=print_graph2(data_train_std,w,ans_train)
    print_graph3(X_train_pca,ans_train)

if __name__ == "__main__":
    main()