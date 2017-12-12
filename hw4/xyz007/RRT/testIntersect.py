import matplotlib.pyplot as plt
import sys
import numpy as np

def line_intersection(line1, line2):
    # xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    # ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    # def det(a, b):
    #     return a[0] * b[1] - a[1] * b[0]

    # div = det(xdiff, ydiff)
    # if div == 0:
    #    return False

    # d = (det(*line1), det(*line2))
    # x = det(d, xdiff) / div
    # y = det(d, ydiff) / div
    # if x >= min(line1[0][0],line1[1][0]) and x <= max(line1[0][0],line1[1][0]) and y >= min(line1[0][1],line1[1][1]) and y <= max(line1[0][1],line1[1][1]):
    #     if x >= min(line2[0][0],line2[1][0]) and x <= max(line2[0][0],line2[1][0]) and y >= min(line2[0][1],line2[1][1]) and y <= max(line2[0][1],line2[1][1]):
    #         return True

    # return False

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
            m = (D[1] - C[1])/(D[0] - C[0])
            b = C[1] - m*C[0]
            yC = C[0] * m + b 
            yD = D[0] * m + b
            if yC == C[1] and yC >= min(A[1],B[1]) and yC <= max(A[1],B[1]) or yD == D[1] and yD >= min(A[1],B[1]) and yD <= max(A[1],B[1]):
                return True

            # print("vertical line1")
            # if min(A[1],B[1]) >= min(C[1],D[1]) and min(A[1],B[1]) <= max(C[1],D[1]) and min(A[0],B[0]) >= min(C[0],D[0]) and min(A[0],B[0]) <= max(C[0],D[0]):
            #     return True
        elif C[0] - D[0] == 0:
            m = (B[1] - A[1])/(B[0] - A[0])
            b = A[1] - m*A[0]
            yA = A[0]*m + b
            yB = B[0]*m + b
            print(A[1])
            if yA == A[1]  and yA >= min(C[1],D[1]) and yA <= max(C[1],D[1]) or yB == B[1] >= min(C[1],D[1]) and yB <= max(C[1],D[1]):
                return True

            # print("vertical line2")
            # if min(C[1],D[1]) >= min(A[1],B[1]) and min(C[1],D[1]) <= max(A[1],B[1]) and min(C[0],D[0]) >= min(A[0],B[0]) and min(C[0],D[0]) <= max(A[0],B[0]):
            #     return True
        elif min(C[0],D[0]) >= min(A[0],B[0]) and min(C[0],D[0]) <= max(A[0],B[0]) or max(C[0],D[0]) >= min(A[0],B[0]) and max(C[0],D[0]) <= max(A[0],B[0]):
            return True            


    if (np.cross(CA,CD).tolist() * np.cross(CB,CD).tolist()) <= 0:
        if (np.cross(AC,AB).tolist() * np.cross(AD,AB).tolist()) <= 0:
            return True

    return False

x1,y1,x2,y2,x3,y3,x4,y4 = float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5]),float(sys.argv[6]),float(sys.argv[7]),float(sys.argv[8])


line1 = [[x1, y1], [x2, y2]]
line2 = [[x3, y3], [x4, y4]]



print(line_intersection(line1,line2))
plt.plot([x1,x2], [y1,y2])
plt.plot([x3,x4],[y3,y4])
plt.show()