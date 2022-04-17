# Open this file with jeroenvantilburg.nl/ppg or any python environment
import matplotlib.pyplot as plt # do not modify; required by ppg
import numpy as np

# Create a numpy array of 500 entries with exponential decay
x = np.linspace(0, 5, 500)
y = np.array(2000 * np.exp(-x)) 

# Create the plot
fig, ax = plt.subplots()
ax.plot(x, y)

# Set the axis
ax.set_xlabel("t (s)", loc='right', fontsize=16)
ax.set_ylabel("N", loc='top', fontsize=16)
ax.set_xlim([0, 5.5])
ax.set_ylim([0, 2100])

# Show the major and minor grid lines
ax.minorticks_on()
ax.grid(which='major', color="grey", alpha=1, lw=0.5)
ax.grid(which='minor', color="grey", alpha=0.5, lw=0.4)

# Remove upper and right axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

plt.show() # last line; do not modify; required by ppg
