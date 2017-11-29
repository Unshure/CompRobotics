import sys
import numpy as np
import math
'''
Report reflexive vertices
'''
def findReflexiveVertices(polygons):
    vertices=[]
    
    # Your code goes here
    # You should return a list of (x,y) values as lists, i.e.
    # vertices = [[x1,y1],[x2,y2],...]

    # Takes cross product of two line segments:
    for polygon in polygons:
        if len(polygon) <4:
            continue
        for index,point in enumerate(polygon):
            p2 = point
            p1 = polygon[(index - 1)%len(polygon)]
            p3 = polygon[(index + 1)%len(polygon)]
            a = np.array([p2[0] - p1[0], p2[1] - p1[1]])
            b = np.array([p3[0] - p2[0], p3[1] - p2[1]])

            # If negative, point is reflexive
            if np.cross(a,b) <0:
                vertices.append(point)
    return vertices

'''
Compute the roadmap graph
'''
def computeSPRoadmap(polygons, reflexVertices):
    vertexMap = dict()
    adjacencyListMap = dict()

    def testIntersect(halfline, edge):
        x1,y1,x2,y2 = halfline[0],halfline[1],halfline[2],halfline[3]
        x3,y3,x4,y4 = edge[0],edge[1],edge[2],edge[3]
        if [x1,y1] == [x3,y3] or [x1,y1] == [x4,y4] or [x2,y2] == [x3,y3] or [x2,y2] == [x4,y4]:
            return False
        if max(x1,x2) < min(x3,x4):
            return False
        if x1-x2 == 0:
            if x3 - x4 != 0:
                if min(x3,x4)<x1 and max(x3,x4)>x1:
                    mline = (y4-y3)/(x4-x3)
                    bline = y3 - mline*x3
                    ycheck = mline * x1 + bline
                    if ycheck > min(y1,y2) and ycheck < max(y1,y2):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            A1 = (y1-y2)/(x1-x2)
        if x3-x4 == 0:
            if x1 - x2 != 0:
                if min(x1,x2) < x3 and max(x1,x2) > x3:
                    mline = (y2-y1)/(x2-x1)
                    bline = y1 - mline*x1
                    ycheck = mline * x3 + bline
                    if ycheck > min(y3,y4) and ycheck < max(y3,y4):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            A2 = (y3-y4)/(x3-x4)
        b1 = y1 - A1*x1
        b2 = y3 - A2*x3
        if A1 == A2:
            return False
        xa = (b2-b1)/(A1 - A2)
        if xa < max(min(x1,x2),min(x3,x4)) or xa > min(max(x1,x2),max(x3,x4)):
             return False
        else:
            return True
    
    #http://cs.smith.edu/~streinu/Teaching/Courses/274/Spring98/Projects/Philip/fp/algVisibility.htm
    #look here for algorithm explination

    # Your code goes here
    # You should check for each pair of vertices whether the
    # edge between them should belong to the shortest path
    # roadmap. 
    #
    # Your vertexMap should look like
    # {1: [5.2,6.7], 2: [9.2,2.3], ... }
    #
    # and your adjacencyListMap should look like
    # {1: [[2, 5.95], [3, 4.72]], 2: [[1, 5.95], [5,3.52]], ... }
    #
    # The vertex labels used here should start from 1
    vertextMap = {}
    #create list of edges
    edgeList = []
    for polygon in polygons:
        for i,point in enumerate(polygon):
            p2 = polygon[(i + 1)%len(polygon)]
            edgeList.append([point[0],point[1],p2[0],p2[1]])

    # Loop though all vert=ices
    index = 0
    for polygon in polygons:
        for indexPoly, point in enumerate([ q for q in polygon if q in reflexVertices]):
            index += 1
            vertexMap[index] = point
            #Initalize list to be put into adjListMap
            pointList = []
            adjList = []

            #Adds Adjacent points to be possible paths
            count = 1
            while polygon[(indexPoly + count)%len(polygon)] not in reflexVertices:
                count +=1
            pointList.append(polygon[(indexPoly + count) % len(polygon)])
            count = 1
            while polygon[(indexPoly - count)%len(polygon)] not in reflexVertices:
                count +=1
            pointList.append(polygon[(indexPoly - count)%len(polygon)])

            for i,point2 in enumerate([ q for q in reflexVertices if q not in polygon]):
                testLine = [point[0], point[1], point2[0], point2[1]]
                for edge in edgeList:
                    #print "TEST STUFF: ",testLine, edge
                    if testIntersect(testLine,edge):
                        #print "intersect"
                        break
                else:
                    #print "free"
                    pointList.append(point2)
            #print pointList
            for x in pointList:
                adjList.append([reflexVertices.index(x)+1, np.linalg.norm(np.array(point) - np.array(x))])
            adjList.sort(key = lambda x: x[0])
            adjacencyListMap[index] = adjList
    return vertexMap, adjacencyListMap

'''
Perform uniform cost search 
'''
def uniformCostSearch(adjListMap, start, goal):
    path = []
    pathLength = 0

    closedSet = set()
    openSet = {start:0}


    # stores like this: {Vertex: [Vertex Parent, length from parent to vertex],...}
    retrace = {}
    def getPath(current):
        reversePath = []
        Length = 0
        reversePath.append(current)
        while current != start:
            reversePath.append(retrace[current][0])
            Length += retrace[current][1]
            current = retrace[current][0]
        reversePath.reverse()
        return reversePath, Length

    while openSet:
        #print openSet 
        current = min(openSet,key = lambda x: openSet[x])
        #print current, openSet
        closedSet.add(current)
        if current == goal:
            #print "I DIDIDIDID ITT"
            path, pathLength = getPath(current)
            break
        for point in adjListMap[current]:
            if point[0] in closedSet:
                continue
            #print point,  retrace[point[0]]
            if point[0] in openSet:
                if point[1] + openSet[current] < openSet[point[0]]:
                    openSet[point[0]] = point[1] + openSet[current]
                    retrace[point[0]] = [current, point[1] + openSet[current]]
                    #print "updated openset" , point[0],  openSet[point[0]]
            else:
                openSet[point[0]] = point[1] + openSet[current]
                retrace[point[0]] = [current, point[1] + openSet[current]]
        del openSet[current]


    
    # Your code goes here. As the result, the function should
    # return a list of vertex labels, e.g.
    #
    # path = [23, 15, 9, ..., 37]
    #
    # in which 23 would be the label for the start and 37 the
    # label for the goal.
    #print path, pathLength
    return path, pathLength

'''
Agument roadmap to include start and goal
'''
def updateRoadmap(polygons, vertexMap, adjListMap, x1, y1, x2, y2):
    updatedALMap = dict()
    startLabel = 0
    goalLabel = -1
    '''
    x1 *= 10
    y1 *= 10
    x2 *= 10
    y2 *= 10
    '''

    def testIntersect(halfline, edge):
        x1,y1,x2,y2 = halfline[0],halfline[1],halfline[2],halfline[3]
        x3,y3,x4,y4 = edge[0],edge[1],edge[2],edge[3]
        if [x1,y1] == [x3,y3] or [x1,y1] == [x4,y4] or [x2,y2] == [x3,y3] or [x2,y2] == [x4,y4]:
            return False
        if max(x1,x2) < min(x3,x4):
            return False
        if x1-x2 == 0:
            if x3 - x4 != 0:
                if min(x3,x4)<x1 and max(x3,x4)>x1:
                    mline = (y4-y3)/(x4-x3)
                    bline = y3 - mline*x3
                    ycheck = mline * x1 + bline
                    if ycheck > min(y1,y2) and ycheck < max(y1,y2):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            A1 = (y1-y2)/(x1-x2)
        if x3-x4 == 0:
            if x1 - x2 != 0:
                if min(x1,x2) < x3 and max(x1,x2) > x3:
                    mline = (y2-y1)/(x2-x1)
                    bline = y1 - mline*x1
                    ycheck = mline * x3 + bline
                    if ycheck > min(y3,y4) and ycheck < max(y3,y4):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            A2 = (y3-y4)/(x3-x4)
        b1 = y1 - A1*x1
        b2 = y3 - A2*x3
        if A1 == A2:
            return False
        xa = (b2-b1)/(A1 - A2)
        if xa < max(min(x1,x2),min(x3,x4)) or xa > min(max(x1,x2),max(x3,x4)):
             return False
        else:
            return True
        
    # Your code goes here. Note that for convenience, we 
    # let start and goal have vertex labels 0 and -1,
    # respectively. Make sure you use these as your labels
    # for the start and goal vertices in the shortest path
    # roadmap. Note that what you do here is similar to
    # when you construct the roadmap. 
    

    edgeList = []
    for polygon in polygons:
        for i,point in enumerate(polygon):
            p2 = polygon[(i + 1)%len(polygon)]
            edgeList.append([point[0],point[1],p2[0],p2[1]])

    polygons.append([[x1,y1]])
    polygons.append([[x2,y2]])
    print polygons
    vertexMap[startLabel] = [x1,y1]
    vertexMap[goalLabel] = [x2,y2]
    
    # Loop though all vertices
    for point in [[x2,y2,goalLabel],[x1,y1,startLabel]]:
        pointList = []
        adjList = []
        #Test for line intersection
        for Rpoint in [ m for m in vertexMap if vertexMap[m] != point[0:2]]:
            testLine = [point[0], point[1], vertexMap[Rpoint][0], vertexMap[Rpoint][1]]
            for edge in edgeList:
                #print "TEST STUFF: ",testLine, edge
                if testIntersect(testLine,edge):
                    #print "intersect"
                    break
            else:
                #print "free"
                pointList.append(Rpoint)
        #print pointList
        for x in pointList:
            eucLen = np.linalg.norm(np.array(point[0:2]) - np.array(vertexMap[x]))
            adjList.append([x, eucLen])
            temp = []
            if x in adjListMap:
                temp = [ m[:] for m in adjListMap[x]]
            temp.append([point[2],eucLen])
            temp.sort(key = lambda x: x[0])
            adjListMap[x] = temp

        adjList.sort(key = lambda x: x[0])
        adjListMap[point[2]] = adjList
        #print adjList

    return startLabel, goalLabel, adjListMap

if __name__ == "__main__":
    
    # Retrive file name for input data
    if(len(sys.argv) < 6):
        print "Five arguments required: python spr.py [env-file] [x1] [y1] [x2] [y2]"
        exit()
    
    filename = sys.argv[1]
    x1 = float(sys.argv[2])
    y1 = float(sys.argv[3])
    x2 = float(sys.argv[4])
    y2 = float(sys.argv[5])

    # Read data and parse polygons
    lines = [line.rstrip('\n') for line in open(filename)]
    polygons = []
    for line in range(0, len(lines)):
        xys = lines[line].split(';')
        polygon = []
        for p in range(0, len(xys)):
            polygon.append(map(float, xys[p].split(',')))
        polygons.append(polygon)

    # Print out the data
    print "Pologonal obstacles:"
    for p in range(0, len(polygons)):
        print str(polygons[p])
    print ""

    # Compute reflex vertices
    reflexVertices = findReflexiveVertices(polygons)
    print "Reflexive vertices:"
    print str(reflexVertices)
    print ""

    # Compute the roadmap 
    vertexMap, adjListMap = computeSPRoadmap(polygons, reflexVertices)
    print "Vertex map:"
    print str(vertexMap)
    print ""
    print "Base roadmap:"
    print str(adjListMap)
    print ""

    # Update roadmap
    start, goal, updatedALMap = updateRoadmap(polygons, vertexMap, adjListMap, x1, y1, x2, y2)
    print "Updated roadmap:"
    print str(updatedALMap)
    print ""

    # Search for a solution     
    path, length = uniformCostSearch(updatedALMap, start, goal)
    print "Final path:"
    print str(path)
    print "Final path length:" + str(length)
    

    # Extra visualization elements goes here

