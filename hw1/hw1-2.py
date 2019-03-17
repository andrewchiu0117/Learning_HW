import numpy as np
def read_data():
    f = open("breast-cancer-wisconsin.data", "r")
    data = []
    for line in f:
        if line.find('?') == -1:
            dd = line[:len(line)-1].split(",", 11)
            count = (int(dd[1]), int(dd[2]), int(dd[3]), int(dd[4]), int(dd[5]), int(dd[6]), int(dd[7]), int(dd[8]), int(dd[9]))
            data.append(count)
    f.close()
    return data

def main():
    data=read_data()
    #print(data)
    x=np.array(data).T
    #print(x)
    print(np.around(np.cov(x),2))

if __name__ == "__main__":
    main()