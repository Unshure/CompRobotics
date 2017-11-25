import sys
'''
x1 = float(sys.argv[1])
y1 = float(sys.argv[2])
x2 = float(sys.argv[3])
y2 = float(sys.argv[4])
x3 = float(sys.argv[5])
y3 = float(sys.argv[6])
x4 = float(sys.argv[7])
y4 = float(sys.argv[8])
'''
def testIntersect(halfline, edge):
    x1,y1,x2,y2 = halfline[0],halfline[1],halfline[2],halfline[3]
    x3,y3,x4,y4 = edge[0],edge[1],edge[2],edge[3]
    if max(x1,x2) <= min(x3,x4):
        return False
    if x1-x2 == 0:
        A1 = float("inf")
    else:
        A1 = (y1-y2)/(x1-x2)
    if x3-x4 == 0:
        A2 = float("inf")
    else:
        A2 = (y3-y4)/(x3-x4)
    b1 = y1 - A1*x1
    b2 = y3 - A2*x3
    if A1 == A2:
        return False
    xa = (b2-b1)/(A1 - A2)
    if xa <= max(min(x1,x2),min(x3,x4)) or xa >= min(max(x1,x2),max(x3,x4)):
         return False
    else:
        return True
print testIntersect([5.2,1.5, 5.2, 4.9], [5.2, 4.9, 5.8, 6.8])