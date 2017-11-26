import sys

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
import spr

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
def createPolygonPatch(polygon):
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
    patch = patches.PathPatch(path, facecolor='gray', lw=1)

    return patch
    
'''
Make a patch for the robot
'''
def createPolygonPatchForRobot(polygon):
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
    patch = patches.PathPatch(path, facecolor='gray', lw=1)

    return patch

'''
Render polygon obstacles  
'''
def drawPolygons(polygons):
    fig, ax = setupPlot()
    for p in range(0, len(polygons)):
        patch = createPolygonPatch(polygons[p])
        ax.add_patch(patch)
    createPaths(polygons)

    plt.show()

def createPaths(polygons):
    x1,y1,x2,y2 = float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5])


    reflexVertices = spr.findReflexiveVertices(polygons)
    vertexMap, adjListMap = spr.computeSPRoadmap(polygons, reflexVertices)
    start, goal, updatedALMap = spr.updateRoadmap(polygons, vertexMap, adjListMap, x1, y1, x2, y2)

    for point in updatedALMap:
        for point2 in updatedALMap[point]:
            p1 = vertexMap[point]
            #print point2
            p2 = vertexMap[point2[0]]
            xvert,yvert = [list(n) for n in zip(p1,p2)]
            plt.plot([xvert[0]/10,xvert[1]/10],[yvert[0]/10,yvert[1]/10],'-g')
    path, length = spr.uniformCostSearch(updatedALMap, start, goal)
    for index in range(0,len(path)-1):
                p1 = vertexMap[path[index]]
                p2 = vertexMap[path[index+1]]
                xvert,yvert = [list(n) for n in zip(p1,p2)]
                plt.plot([xvert[0]/10,xvert[1]/10],[yvert[0]/10,yvert[1]/10],'-r')

if __name__ == "__main__":
    
    # Retrive file name for input data
    if(len(sys.argv) < 2):
        print "Please provide inpu tfile: python visualize.py [env-file]"
        exit()
    
    filename = sys.argv[1]

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
    for p in range(0, len(polygons)):
        print str(polygons[p])

    # Draw the polygons
    drawPolygons(polygons)

    
