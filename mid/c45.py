import math

def entropy(x,y):
    if y==0 and x!=0:
        return -x/(x+y)*math.log(x/(x+y),2)
    elif x==0 and y!=0:
        return -y/(x+y)*math.log(y/(x+y),2)
    elif x==0 and y==0:
        return 0
    else:
        return -x/(x+y)*math.log(x/(x+y),2)-y/(x+y)*math.log(y/(x+y),2)

def gain(x1,x2,y1,y2): #1_play,2_total
    return entropy(x1+y1,x2+y2-(x1+y1))-(x2/(x2+y2))*entropy(x1,x2-x1)-(y2/(x2+y2))*entropy(y1,y2-y1)


def gain_radio(x1,x2,y1,y2):
    return gain(x1,x2,y1,y2)/entropy(x2,y2)



print(gain_radio(5,8,4,6))
print(gain_radio(7,9,2,5))