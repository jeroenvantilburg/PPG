# Open this file with jeroenvantilburg.nl/ppg or any python environment
import matplotlib.pyplot as plt # do not modify; required by ppg
import numpy as np
from math import *

# Create a numpy array of 400 entries with a sinus
x = np.linspace(0, 7, 400)
y = -0.75*np.cos(2*pi*x)

fig, ax = plt.subplots()
ax.plot(x, y)

# Set the axes
ax.set_xlim([0, 1.2])
ax.set_ylim([-1, 1])
ax.set_xlabel("tijd (s)", loc='right', fontsize=14)
ax.set_ylabel( "U (V)", loc='top', fontsize=14)

# Show the minor ticks and the major grid
ax.minorticks_on()
ax.grid(which='major')

# Move bottom x-axis to centre, passing through (0,0)
ax.spines['bottom'].set_position('center')

# Eliminate upper and right axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')


plt.show() # last line; do not modify; required by ppg
