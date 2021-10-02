import matplotlib.pyplot as plt

import numpy as np
from math import *

x = np.linspace(0, 7, 400)
y = np.sin(2*pi*0.882*x)

fig = plt.figure()
plt.plot(x, y)

plt.xlabel("tijd (ms)", loc='right')
plt.ylabel("u (mV)", loc='top')

plt.minorticks_on()
plt.grid(which='major')

ax = fig.add_subplot(1, 1, 1)

# Move left y-axis and bottim x-axis to centre, passing through (0,0)
#ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')

# Eliminate upper and right axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

# Show ticks in the left and lower axes only
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.set_xlim([0, 7.8])

plt.show()
