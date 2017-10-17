import sys
import numpy as np
import matplotlib.pyplot as plt

def trilaterate3D(distances):
    p1 = np.array(distances[0][0:3])
    p2 = np.array(distances[1][0:3])
    p3 = np.array(distances[2][0:3])
    p4 = np.array(distances[3][0:3])
    r1 = distances[0][3]
    r2 = distances[1][3]
    r3 = distances[2][3]
    r4 = distances[3][3]
    x,y,z = 0,0,0

    ex = (p2-p1)/(np.linalg.norm(p2-p1))
    i =  np.dot(ex, (p3-p1))

    ey = (p3-p1 -i*ex)/(np.linalg.norm(p3-p1-i*ex))

    ez = np.cross(ex,ey)

    d = np.linalg.norm(p2-p1)
    # cj was chosed instad of j since j represents complex numbers
    cj = np.dot(ey,(p3-p1))

    x = (np.power(r1,2) - np.power(r2,2) + np.power(d,2))/(2*d)
    y = (np.power(r1,2)-np.power(r3,2)+np.power(i,2)+np.power(cj,2))/(2*cj) - (i*x)/(cj)
    zPos = np.sqrt(np.power(r1,2)-np.power(x,2)-np.power(y,2))
    zNeg = -1*np.sqrt(np.power(r1,2)-np.power(x,2)-np.power(y,2))

    pPos = p1 + x*ex + y*ey + zPos*ez
    pNeg = p1 + x*ex + y*ey + zNeg*ez

    if abs(np.linalg.norm(abs(p4-pPos)) -r4) > abs(np.linalg.norm(abs(p4-pNeg)) -r4):
        return pPos
    else:
        return pNeg


if __name__ == "__main__":
    
    # Retrive file name for input data
    if(len(sys.argv) == 1):
        print "Please enter data file name."
        exit()
    
    filename = sys.argv[1]

    # Read data
    lines = [line.rstrip('\n') for line in open(filename)]
    distances = []
    for line in range(0, len(lines)):
        distances.append(map(float, lines[line].split(' ')))
    # Print out the data
    print "The input four points and distances, in the format of [x, y, z, d], are:"
    for p in range(0, len(distances)):
        print distances[p] 
    # Call the function and compute the location  
    location = trilaterate3D(distances)
    print 
    print "The location of the point is: " + str(location)
