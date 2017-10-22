import sys
import matplotlib.pyplot as plt
import numpy as np
if __name__ == "__main__":
    
    # Retrive file name for input data
    if(len(sys.argv) < 5):
        print "Four arguments required: python kalman2d.py [datafile] [x1] [x2] [lambda]"
        exit()
    
    filename = sys.argv[1]
    x10 = float(sys.argv[2])
    x20 = float(sys.argv[3])
    scaler = float(sys.argv[4])

    # Read data
    lines = [line.rstrip('\n') for line in open(filename)]
    data = []
    for line in range(0, len(lines)):
        data.append(map(float, lines[line].split(' ')))

    measured1 = []
    measured2 = []

    Kk = np.eye(2)
    P = scaler*np.eye(2)
    xhat = np.array([[x10],[x20]])
    Qcovar = np.array([[10**-4, 2*10**-5],[2*10**-5,10**-4]])
    Rcovar = np.array([[10**-2, 5*10**-3],[5*10**-3,2*10**-2]])
    pred1 = []
    pred2 = []
    # Print out the data
    print "The input data points in the format of 'k [u1, u2, z1, z2]', are:"
    for it in range(0, len(data)):
        print str(it + 1) + " " + str(data[it])
        measured1.append(data[it][2])
        measured2.append(data[it][3])

        ####Kalman Filter

        #Time Update
        u_1 = np.array([[data[it][0]],[data[it][1]]])
        xhat_ = xhat + u_1
        P_ = P + Qcovar

        #Measurement Update
        z = np.array([[data[it][2]],[data[it][3]]])
        Kk = np.dot(P_,np.linalg.inv((P_ + Rcovar)))
        xhat = xhat_ + np.dot(Kk,(z - xhat_))        
        P = np.dot((np.eye(2) - Kk),P_)

        pred1.append(xhat[0])
        pred2.append(xhat[1])

    plt.plot(measured1,measured2, 'r', pred1, pred2, 'g')
    plt.show()
