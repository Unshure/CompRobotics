import sys



def checkIntersect(line1, line2):
	xdiff = (line1[0] - line1[2], line2[0] - line2[2])
	ydiff = (line1[1] - line1[3], line2[1] - line2[3])

	def det2d(x,y):
		return x[0]*y[1] - y[0] * x[1]

	print(det2d(xdiff,ydiff))
	if det2d(xdiff, ydiff) == 0:
		return False
	else:
		return True


line1 = (float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
line2 = (float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8]))

print(checkIntersect(line1,line2))