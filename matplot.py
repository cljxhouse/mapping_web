# -*- encoding: utf-8 -*-

import matplotlib as mpl
import matplotlib.pyplot as plt

x=[1,2,3,4,5]
y=[2,3,4,5,6]
#color=[[(lambda x:x*x)(x) for x in range(1,11)]]
color=['r','r','r','r','b']

plt.scatter(x,y,c=color)
plt.show()