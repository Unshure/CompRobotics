import matplotlib.pyplot as plt
import sys

def line_intersection(line1, line2):
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

x1,y1,x2,y2,x3,y3,x4,y4 = float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5]),float(sys.argv[6]),float(sys.argv[7]),float(sys.argv[8])


line1 = [[x1, y1], [x2, y2]]
line2 = [[x3, y3], [x4, y4]]



print(line_intersection(line1,line2))
plt.plot([x1,x2], [y1,y2])
plt.plot([x3,x4],[y3,y4])
plt.show()