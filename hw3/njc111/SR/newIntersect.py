import sys

x1 = float(sys.argv[1])
y1 = float(sys.argv[2])
x2 = float(sys.argv[3])
y2 = float(sys.argv[4])
x3 = float(sys.argv[5])
y3 = float(sys.argv[6])
x4 = float(sys.argv[7])
y4 = float(sys.argv[8])





def line_intersection(halfLine, edge):
    x1,y1,x2,y2 = halfLine[0],halfLine[1],halfLine[2],halfLine[3]
    x3,y3,x4,y4 = edge[0],edge[1],edge[2],edge[3]
    if [x1,y1] == [x3,y3] or [x1,y1] == [x4,y4] or [x2,y2] == [x3,y3] or [x2,y2] == [x4,y4]:
        return False
    line1 = [[halfLine[0],halfLine[1]],[halfLine[2],halfLine[3]]]
    line2 = [[edge[0],edge[1]],[edge[2],edge[3]]]
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return True

    div = det(xdiff, ydiff)
    if div == 0:
        return False
    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return True

print line_intersection([x1,y1,x2,y2],[x3,y3,x4,y4])