import numpy as np
import sys



def growSimpleRRT(points):
    newPoints = dict()
    adjListMap = dict()
    # Your code goes here
    newPoints[1] = points[1]
    adjListMap[1] = []

    segList = [[0,0,2,0]]

    point = {1: ()}


    for x,y in [points[pt] for pt in point]:
    	# line format = [x1 y1 x2 y2]
    	for line in segList:
    		ax = x - line[0]
    		ay = y - line[1]
    		bx = line[3] - line[0]
    		by = line[4] - line[1]
    		print np.dot([ax,ay],[bx,by])




    return newPoints, adjListMap



#def closestPoint(x,y,line):


# Example points for calling growSimpleRRT
# You should expect many mroe points, e.g., 200-500
points = dict()
points[1] = (5, 5)
points[2] = (7, 8.2)
points[3] = (6.5, 5.2)
points[4] = (0.3, 4)
points[5] = (6, 3.7)
points[6] = (9.7, 6.4)
points[7] = (4.4, 2.8)
points[8] = (9.1, 3.1)
points[9] = (8.1, 6.5)
points[10] = (0.7, 5.4)
points[11] = (5.1, 3.9)
points[12] = (2, 6)
points[13] = (0.5, 6.7)
points[14] = (8.3, 2.1)
points[15] = (7.7, 6.3)
points[16] = (7.9, 5)
points[17] = (4.8, 6.1)
points[18] = (3.2, 9.3)
points[19] = (7.3, 5.8)
points[20] = (9, 0.6)

# Printing the points
print "" 
print "The input points are:"
print str(points)
print ""

points, adjListMap = growSimpleRRT(points)

print "These are the points: ", points

print "This is the adjList: ", adjListMap
