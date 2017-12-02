import sys

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib import collections  as mc
import numpy as np
import math
import random

'''
Set up matplotlib to create a plot with an empty square
'''
def setupPlot():
    fig = plt.figure(num=None, figsize=(5, 5), dpi=120, facecolor='w', edgecolor='k')
    plt.autoscale(False)
    plt.axis('off')
    ax = fig.add_subplot(1,1,1)
    ax.set_axis_off()
    ax.add_patch(patches.Rectangle(
        (0,0),   # (x,y)
        1,          # width
        1,          # height
        fill=False
        ))
    return fig, ax

'''
Make a patch for a single pology
'''
def createPolygonPatch(polygon, color):
    verts = []
    codes= []
    for v in range(0, len(polygon)):
        xy = polygon[v]
        verts.append((xy[0]/10., xy[1]/10.))
        if v == 0:
            codes.append(Path.MOVETO)
        else:
            codes.append(Path.LINETO)
    verts.append(verts[0])
    codes.append(Path.CLOSEPOLY)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor=color, lw=1)

    return patch


'''
Render the problem
'''
def drawProblem(robotStart, robotGoal, polygons):
    fig, ax = setupPlot()
    patch = createPolygonPatch(robotStart, 'green')
    ax.add_patch(patch)
    patch = createPolygonPatch(robotGoal, 'red')
    ax.add_patch(patch)
    for p in range(0, len(polygons)):
        patch = createPolygonPatch(polygons[p], 'gray')
        ax.add_patch(patch)
    plt.show()

def find_closest_point(P0, P1, P2):

    P0 = np.array(P0)
    P1 = np.array(P1)
    P2 = np.array(P2)

    A = P2 - P0
    B = P1 - P0

    B_inverse = P0 - P1
    C = P2 - P1

    world_frame = np.array([1,0]) - np.array([0,0])

    ab_dot = np.dot(A,B)
    cb_dot = np.dot(B_inverse,C)

    #Point is over the line
    if(ab_dot > 0 and cb_dot > 0):
        projection = ab_dot/np.linalg.norm(B)
        angle = np.degrees(math.acos(np.dot(B,world_frame)/(np.linalg.norm(B) * np.linalg.norm(world_frame))))
        # angle = np.degrees(math.acos(np.dot(B,world_frame)/(np.linalg.norm(B) * np.linalg.norm(world_frame))))
        distance = math.sqrt(math.pow(np.linalg.norm(A),2) - math.pow(projection,2))

        # new_point = [projection * math.cos(np.deg2rad(angle)), projection * math.sin(np.deg2rad(angle))] + P0

        if (P1[1] - P0[1]) >= 0:
            new_point = [projection * math.cos(np.deg2rad(angle)), projection * math.sin(np.deg2rad(angle))] + P0
        else:
            new_point = P0 - [projection * math.cos(np.deg2rad(180 - angle)), projection * math.sin(np.deg2rad(180 - angle))]

        # print("New point location: {}".format(new_point))
        # print("Distance to line: {}".format(distance))

        return new_point, True, distance

    #Point is closer to vertex
    else:
        distance_to_P0 = dist = np.linalg.norm(P2-P0)
        distance_to_P1 = dist = np.linalg.norm(P2-P1)

        if distance_to_P0 <= distance_to_P1:
            # print("Distance to P0 is closer: {}".format(distance_to_P0))
            return P0, False, distance_to_P0
        else:
            # print("Distance to P1 is closer: {}".format(distance_to_P1))
            return P1, False, distance_to_P1

'''
Grow a simple RRT
'''
def growSimpleRRT(points):
    newPoints = dict()
    adjListMap = dict()
    segment_list = []

    #Connect first two points by default
    newPoints[1] = points[1]
    newPoints[2] = points[2]

    adjListMap[1] = [2]
    adjListMap[2] = []

    new_segment = dict()
    new_segment['point1'] = 1
    new_segment['point2'] = 2
    new_segment['line'] = [points[1],points[2]]

    segment_list.append(new_segment)

    for point_index in range(3,len(points) + 1):
        point = points[point_index]

        #Add it to the new_points_list
        index = len(newPoints)+1
        newPoints[index] = point

        adjListMap[index] = []

        closest_distance = float("inf")
        closest_point_index = -1
        final_closest_point = [-1,-1]
        final_is_new = False
        closest_point_1 = []
        closest_point_2 = []

        # print("\n\n Here")
        # print(segment_list)

        for segment in segment_list:

            point_1 = segment['point1']
            point_2 = segment['point2']
            line = segment['line']
            closest_point, is_new_point, distance = find_closest_point(line[0], line[1], point)

            # print("Meow Meow")
            # print("New: {}, Segment {} -> {}, Closest: {}, IsNew: {}, Distance: {}").format(point, line[0], line[1], closest_point, is_new_point, distance)

            closest_index = [-1,-1]

            if np.array_equal(closest_point,line[0]):
                closest_index = point_1
            elif np.array_equal(closest_point,line[1]):
                closest_index = point_2

            if distance < closest_distance:
                closest_distance = distance
                closest_point_index = closest_index
                final_closest_point = closest_point
                final_is_new = is_new_point
                closest_point_1 = point_1
                closest_point_2 = point_2

        if final_is_new:
            new_point_index = len(newPoints)+1
            newPoints[new_point_index] = final_closest_point

            adjListMap[new_point_index] = [index]

            new_segment = dict()
            new_segment['point1'] = new_point_index
            new_segment['point2'] = index
            new_segment['line'] = [newPoints[new_point_index], newPoints[index]]
            segment_list.append(new_segment)

            if closest_point_2 in adjListMap[closest_point_1]:
                adjListMap[closest_point_1].remove(closest_point_2)

                for index, segment in enumerate(segment_list):
                    if segment['point1'] == closest_point_1 and segment['point2'] == closest_point_2:
                        del(segment_list[index])

                adjListMap[closest_point_1].append(new_point_index)
                adjListMap[new_point_index].append(closest_point_2)

                new_segment = dict()
                new_segment['point1'] = closest_point_1
                new_segment['point2'] = new_point_index
                new_segment['line'] = [newPoints[closest_point_1],newPoints[new_point_index]]
                segment_list.append(new_segment)

                new_segment = dict()
                new_segment['point1'] = new_point_index
                new_segment['point2'] = closest_point_2
                new_segment['line'] = [newPoints[new_point_index],newPoints[closest_point_2]]
                segment_list.append(new_segment)

            elif closest_point_1 in adjListMap[closest_point_2]:
                adjListMap[closest_point_2].remove(closest_point_1)
                adjListMap[closest_point_2].append(new_point_index)
                adjListMap[new_point_index].append(closest_point_1)

                for index, segment in enumerate(segment_list):
                    if segment['point1'] == closest_point_2 and segment['point2'] == closest_point_1:
                        del(segment_list[index])

                new_segment = dict()
                new_segment['point1'] = closest_point_2
                new_segment['point2'] = new_point_index
                new_segment['line'] = [newPoints[closest_point_2],newPoints[new_point_index]]
                segment_list.append(new_segment)

                new_segment = dict()
                new_segment['point1'] = new_point_index
                new_segment['point2'] = closest_point_1
                new_segment['line'] = [newPoints[new_point_index],newPoints[closest_point_1]]
                segment_list.append(new_segment)

        else: #Not new point
            adjListMap[closest_point_index].append(index)
            new_segment = dict()
            new_segment['point1'] = closest_point_index
            new_segment['point2'] = index
            new_segment['line'] = [newPoints[closest_point_index],newPoints[index]]
            segment_list.append(new_segment)

    # print(adjListMap)

    return newPoints, adjListMap

'''
Perform basic search
'''
def basicSearch(tree, start, goal):
    path = []

    # Your code goes here. As the result, the function should
    # return a list of vertex labels, e.g.
    #
    # path = [23, 15, 9, ..., 37]
    #
    # in which 23 would be the label for the start and 37 the
    # label for the goal.

    queue = []
    closed_list = dict()

    #Add the start to the goal
    queue.append((start,None))
    while(len(queue) != 0):
        # current_distance, potential_node, parent = heapq.heappop(queue)
        potential_node, parent = queue.pop(0)

        if(potential_node not in closed_list):
        # if(closed_list[potential_node] != None):
            closed_list[potential_node] = parent
            # pathLength = current_distance
            if potential_node == goal:
                break;
            neighbors = adjListMap[potential_node]
            for neighbor in neighbors:
                # neighbor_index = neighbor[0]
                # neighbor_distance = neighbor[1]
                if neighbor not in closed_list:
                # if closed_list[neighbor_index] != None:
                    queue.append((neighbor,potential_node))
                    # heapq.heappush(queue, (neighbor_distance + current_distance,neighbor_index, potential_node))

    index = goal
    while True:
        path.insert(0, index)
        index = closed_list[index]
        if index == None:
            break

    print("This: {}").format(path)

    return path

'''
Display the RRT and Path
'''
def displayRRTandPath(points, tree, path, robotStart = None, robotGoal = None, polygons = None):

    # Your code goes here
    # You could start by copying code from the function
    # drawProblem and modify it to do what you need.
    # You should draw the problem when applicable.

    lines = []
    path_lines = []

    for parent in tree:
        for kid in tree[parent]:

            point_1 = points[parent]
            point_2 = points[kid]
            lines.append([[point_1[0]/10.00, point_1[1]/10.00], [point_2[0]/10.00, point_2[1]/10.00]])

    for parent in path:
        for kid in tree[parent]:

            point_1 = points[parent]
            point_2 = points[kid]
            path_lines.append([[point_1[0]/10.00, point_1[1]/10.00], [point_2[0]/10.00, point_2[1]/10.00]])

    lc = mc.LineCollection(lines)
    pc = mc.LineCollection(path_lines, colors='green', linewidths=4)

    print(path)

    fig, ax = setupPlot()
    ax.add_collection(lc)
    ax.add_collection(pc)

    plt.show()

    return

'''
Collision checking
'''
def isCollisionFree(robot, point, obstacles):

    # Your code goes here.

    return False

'''
The full RRT algorithm
'''
def RRT(robot, obstacles, startPoint, goalPoint):

    points = dict()
    tree = dict()
    path = []
    # Your code goes here.

    return points, tree, path

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

    # Visualize
    robotStart = []
    robotGoal = []

    def start((x,y)):
        return (x+x1, y+y1)
    def goal((x,y)):
        return (x+x2, y+y2)
    robotStart = map(start, robot)
    robotGoal = map(goal, robot)
    drawProblem(robotStart, robotGoal, obstacles)

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

    # for i in range(1,300):
    #     point_x = random.uniform(0, 10)
    #     point_y = random.uniform(0, 10)
    #     points[i] = (point_x, point_y)

    # points[1] = (4.9, 5)
    # points[2] = (5, 7)
    # points[3] = (6, 6)

    # points[4] = (7, 7)
    # points[5] = (6, 8)
    # points[6] = (8, 8)
    # points[7] = (7.3, 6.5)
    # points[8] = (7, 7.5)
    # points[9] = (6, 6.5)

    # Printing the points
    print ""
    print "The input points are:"
    print str(points)
    print ""

    points, adjListMap = growSimpleRRT(points)

    # Search for a solution
    path = basicSearch(adjListMap, 1, 20)

    print("1: {}").format(path)

    # Your visualization code
    displayRRTandPath(points, adjListMap, path)

    # Solve a real RRT problem
    RRT(robot, obstacles, (x1, y1), (x2, y2))

    # Your visualization code
    displayRRTandPath(points, adjListMap, path, robotStart, robotGoal, obstacles)
