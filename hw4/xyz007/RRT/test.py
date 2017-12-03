import numpy
import math

#Overline
# P0 = numpy.array([0,0])
# P1 = numpy.array([2,0])
# P2 = numpy.array([1,2])

#Overline - line is angled 45deg
P0 = numpy.array([6.5,5.2])
P1 = numpy.array([6.5,3.7])
P2 = numpy.array([9.1,3.1])

#To Left of line
# P0 = numpy.array([1,0])
# P1 = numpy.array([2,0])
# P2 = numpy.array([0,1])

#P0 -> P1 (Segment), P2 (New Point)
def closest_point(P0, P1, P2):

    A = P2 - P0
    B = P1 - P0

    B_inverse = P0 - P1
    C = P2 - P1

    world_frame = numpy.array([1,0]) - numpy.array([0,0])

    ab_dot = numpy.dot(A,B)
    cb_dot = numpy.dot(B_inverse,C)

    print(ab_dot, cb_dot)

    #Point is over the line
    if(ab_dot > 0 and cb_dot > 0):

        projection = ab_dot/numpy.linalg.norm(B)
        angle = numpy.degrees(math.acos(numpy.dot(B,world_frame)/(numpy.linalg.norm(B) * numpy.linalg.norm(world_frame))))
        distance = math.sqrt(math.pow(numpy.linalg.norm(A),2) - math.pow(projection,2))

        print(angle)

        if (P1[1] - P0[1]) >= 0 and (P1[0] - P0[0]):
            new_point = [projection * math.cos(numpy.deg2rad(angle)), projection * math.sin(numpy.deg2rad(angle))] + P0
        else:
            new_point = P0 - [projection * math.cos(numpy.deg2rad(180 - angle)), projection * math.sin(numpy.deg2rad(180 - angle))]

        print("New point location: {}".format(new_point))
        print("Distance to line: {}".format(distance))

        return new_point, True

    #Point is closer to vertex
    else:
        distance_to_P0 = dist = numpy.linalg.norm(P2-P0)
        distance_to_P1 = dist = numpy.linalg.norm(P2-P1)

        if distance_to_P0 <= distance_to_P1:
            print("Distance to P0 is closer: {}".format(distance_to_P0))
            return P0, False
        else:
            print("Distance to P1 is closer: {}".format(distance_to_P1))
            return P1, False

closest_point(P0,P1,P2)
