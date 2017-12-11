import sys

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib import collections  as mc
import numpy as np
import math
import random



def checkIntersect(line1, line2):
    A = np.array([line1[0][0],line1[0][1]])
    B = np.array([line1[1][0],line1[1][1]])
    C = np.array([line2[0][0],line2[0][1]])
    D = np.array([line2[1][0],line2[1][1]])

    CA = A-C
    CD = D-C
    CB = B-C

    AC = C-A
    AD = D-A
    AB = B-A


    cross1 = np.cross(CA,CD).tolist()
    cross2 = np.cross(CB,CD).tolist()
    cross3 = np.cross(AC,AB).tolist()
    cross4 = np.cross(AD,AB).tolist()

    print("Cross: ", cross1, cross2, cross3, cross4)

    #parallel
    if cross1 == 0 and cross2 == 0 and cross3 == 0 and cross4 == 0:
        print("parallel")
        #Vertical Line
        if A[0] - B[0] == 0:
            if min(C[1],D[1]) >= min(A[1],B[1]) and min(C[1],D[1]) <= max(A[1],B[1]):
                return True
        elif min(C[0],D[0]) >= min(A[0],B[0]) and min(C[0],D[0]) <= max(A[0],B[0]):
            return True

    #One point touches
    if cross1 == 0 or cross2 == 0 or cross3 == 0 or cross4 == 0:
        print("One touch")
        #vertical case
        if A[0] - B[0] == 0:
            xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
            ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

            def det(a, b):
                return a[0] * b[1] - a[1] * b[0]

            div = det(xdiff, ydiff)
            if div == 0:
               return False

            d = (det(*line1), det(*line2))
            x = det(d, xdiff) / div
            y = det(d, ydiff) / div
            if x >= min(line1[0][0],line1[1][0]) and x <= max(line1[0][0],line1[1][0]) and y >= min(line1[0][1],line1[1][1]) and y <= max(line1[0][1],line1[1][1]):
                if x >= min(line2[0][0],line2[1][0]) and x <= max(line2[0][0],line2[1][0]) and y >= min(line2[0][1],line2[1][1]) and y <= max(line2[0][1],line2[1][1]):
                    return True

            return False

            # m = (D[1] - C[1])/(D[0] - C[0])
            # b = C[1] - m*C[0]
            # if (A[0] * m + b) == A[1] or (B[0] * m + b) == B[1]:
            #     return True
            # print("vertical line1")
            # if min(A[1],B[1]) >= min(C[1],D[1]) and min(A[1],B[1]) <= max(C[1],D[1]) and min(A[0],B[0]) >= min(C[0],D[0]) and min(A[0],B[0]) <= max(C[0],D[0]):
            #     return True
        elif C[0] - D[0] == 0:
            #Frankinstien Code:
            xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
            ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

            def det(a, b):
                return a[0] * b[1] - a[1] * b[0]

            div = det(xdiff, ydiff)
            if div == 0:
               return False

            d = (det(*line1), det(*line2))
            x = det(d, xdiff) / div
            y = det(d, ydiff) / div
            if x >= min(line1[0][0],line1[1][0]) and x <= max(line1[0][0],line1[1][0]) and y >= min(line1[0][1],line1[1][1]) and y <= max(line1[0][1],line1[1][1]):
                if x >= min(line2[0][0],line2[1][0]) and x <= max(line2[0][0],line2[1][0]) and y >= min(line2[0][1],line2[1][1]) and y <= max(line2[0][1],line2[1][1]):
                    return True

            return False


            # m = (B[1] - A[1])/(B[0] - A[0])
            # b = A[1] - m*A[0]
            # if (C[0] * m + b) == C[1] or (D[0] * m + b) == D[1]:
            #     return True

            # print("vertical line2")
            # if min(C[1],D[1]) >= min(A[1],B[1]) and min(C[1],D[1]) <= max(A[1],B[1]) and min(C[0],D[0]) >= min(A[0],B[0]) and min(C[0],D[0]) <= max(A[0],B[0]):
            #     return True
        elif min(C[0],D[0]) >= min(A[0],B[0]) and min(C[0],D[0]) <= max(A[0],B[0]) or max(C[0],D[0]) >= min(A[0],B[0]) and max(C[0],D[0]) <= max(A[0],B[0]):
            return True            


    if (np.cross(CA,CD).tolist() * np.cross(CB,CD).tolist()) < 0:
        if (np.cross(AC,AB).tolist() * np.cross(AD,AB).tolist()) < 0:
            return True

    return False

def isCollisionFree(robot, point, obstacles):
    # print(point)
    obstList = []

    for obstacle in obstacles:
        for index,pt1 in enumerate(obstacle):
            nextindex = (index+1)%len(obstacle)
            obstList.append([[pt1[0],pt1[1]],[obstacle[nextindex][0],obstacle[nextindex][1]]])
    obstList.append([[0,0],[0,10]])
    obstList.append([[0,10],[10,10]])
    obstList.append([[10,10],[10,0]])
    obstList.append([[0,0],[10,0]])


    for i,p in enumerate(robot):
        nexti = (i+1) % len(robot)
        roboedge = [[point[0] + p[0],point[1] + p[1]],[point[0] +robot[nexti][0],point[1] + robot[nexti][1]]]
        print("this is roboedge " ,roboedge)
        for edge in obstList:
            # print(roboedge)
            # print(edge)
            if checkIntersect(roboedge,edge):
                print("Collides with: ", edge)
                # print(roboedge)
                # print(edge)
                return False
    return True


if __name__ == "__main__":

    # Retrive file name for input data
    if(len(sys.argv) < 2):
        print "Five arguments required: python spr.py [env-file] [x1] [y1] [x2] [y2]"
        exit()

    filename = sys.argv[1]

    # Read data and parse polygons
    lines = [line.rstrip('\n') for line in open(filename)]
    robot = []
    obstacles = []
    for line in range(0, len(lines)):
        xys = lines[line].split(';')
        polygon = []
        for p in range(0, len(xys)):
            xy = xys[p].split(',')
            polygon.append((float(xy[0]), float(xy[1])))
        if line == 0 :
            robot = polygon
        else:
            obstacles.append(polygon)

    # Print out the data
    print "Robot:"
    print str(robot)
    print "Pologonal obstacles:"
    for p in range(0, len(obstacles)):
        print str(obstacles[p])
    print ""

    print(isCollisionFree(robot, (1,1),obstacles))