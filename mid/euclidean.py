import numpy
import math

def euclidean_distance(m1, m2): #算距離
    v1=numpy.array(m1)
    v2=numpy.array(m2)
    distance = numpy.linalg.norm(v1 - v2)
    return distance

def main():
    r=1
    for k in range(0,24):
        print(r*math.cos(2*math.pi*k/24))



if __name__ == "__main__":
    main()