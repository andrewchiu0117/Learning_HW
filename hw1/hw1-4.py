import numpy as np
def read_data(): #讀檔案
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
    v1=np.array(data).T
    v3=np.corrcoef(v1)
    print(np.around(v3, 2))
    for x in range(9):
        count=[]
        for y in range(9):
            if v3[x][y] > 0.5 and x!=y:
                count.append(y+2)
        if len(count)!=0:
            print(x+2,"has strong connection with",count)
        else:
            print(x+2,"has no strong connection")

if __name__ == "__main__":
    main()