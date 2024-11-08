# -*- coding: utf-8 -*-
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from numpy import genfromtxt  # Sửa import từ numpy thay vì scipy

# read csv file
d = genfromtxt("input/code_test.csv", delimiter=",")

# make graph
fig = pyplot.figure()
ax = Axes3D(fig)

# setting graph
ax.set_xlabel("Green")
ax.set_ylabel("Blue")
ax.set_zlabel("Red")

# plot
ax.plot(d[:,1], d[:,0], d[:,2], "o", color="#ff0000", ms=4, mew=0.5)

pyplot.show()
