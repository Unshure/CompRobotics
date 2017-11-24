import sys
import math

x = float(sys.argv[1])
y = float(sys.argv[2])

#a = math.degrees(math.atan(y/x)) + (x/abs(x) -1)*-90 + (x/abs(x) +1)*(y/abs(y) -1)*-90
if x ==0:
	if y >0:
		print 90
	else:
		print 270
if y==0:
	if x>0:
		print 0
	else:
		print 180
a = math.degrees(math.atan(y/x))
if x<0:
	a = a+180
elif y<0:
	a = a+360

print a