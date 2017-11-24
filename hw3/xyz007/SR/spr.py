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
    #Returns angle from the x axis ccw
    def getAngle(point):
        x = point[0] - p[0]
        y = point[1] - p[1]
        if x ==0:
            if y >0:
                return 90
            else:
                return 270
        if y==0:
            if x>0:
                return 0
            else:
                return 180
        a = math.degrees(math.atan(y/x))
        if x<0:
            a = a+180
        elif y<0:
            a = a+360
        return a

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
    adjListMap = {}
    vertextMap = {}
    #create list of edges
    edgeList = []
    for polygon in polygons:
        for i,point in enumerate(polygon):
            p2 = polygon[(i + 1)%len(polygon)]
            edgeList.append([point[0],point[1],p2[0],p2[1]])
         

    # Loop though all vertices
    for index,p in enumerate(reflexVertices):
        vertexMap[index+1] = p

        #Sort in clockwise order
        #listclock = [n[:] for n in reflexVertices]
        #listclock.pop(listclock.index(p))
        #listclock.sort(key = getAngle, reverse = True)

        #Initalize list to be put into adjListMap
        adjList = []
        # Test for visibility
        for i,point in enumerate(reflexVertices):
            if point == p:
                continue
            testLine = [p[0],p[1],point[0],point[1]]
            for edge in edgeList:
                print "TEST STUFF: ",testLine, edge
                if testIntersect(testLine,edge):
                    break
            else:
                adjList.append([i+1,np.linalg.norm(np.array(point) - np.array(p))])
        adjList.sort(key = lambda x: x[0])
        adjListMap[index+1] = adjList
        
    return vertexMap, adjListMap

'''
Perform uniform cost search 
'''
def uniformCostSearch(adjListMap, start, goal):
    path = []
    pathLength = 0
    
    # Your code goes here. As the result, the function should
    # return a list of vertex labels, e.g.
    #
    # path = [23, 15, 9, ..., 37]
    #
    # in which 23 would be the label for the start and 37 the
    # label for the goal.
    
    return path, pathLength

'''
Agument roadmap to include start and goal
'''
def updateRoadmap(adjListMap, x1, y1, x2, y2):
    updatedALMap = dict()
    startLabel = 0
    goalLabel = -1

    # Your code goes here. Note that for convenience, we 
    # let start and goal have vertex labels 0 and -1,
    # respectively. Make sure you use these as your labels
    # for the start and goal vertices in the shortest path
    # roadmap. Note that what you do here is similar to
    # when you construct the roadmap. 
    
    return startLabel, goalLabel, updatedALMap

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
    start, goal, updatedALMap = updateRoadmap(adjListMap, x1, y1, x2, y2)
    print "Updated roadmap:"
    print str(updatedALMap)
    print ""

    # Search for a solution     
    path, length = uniformCostSearch(updatedALMap, start, goal)
    print "Final path:"
    print str(path)
    print "Final path length:" + str(length)
    

    # Extra visualization elements goes here
