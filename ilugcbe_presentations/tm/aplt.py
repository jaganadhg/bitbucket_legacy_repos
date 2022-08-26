#!/usr/bin/env python
from pylab import figure, show
import numpy as np
width = 0.5
xs = np.arange(7)
ys = xs

fig = figure()
ax = fig.add_subplot(111)
ax.bar(xs, ys, width=width)

for x,y in zip(xs, ys):
    ax.text(x+width/2., y, '%1.1f'%y, va='bottom', ha='center')

show()
