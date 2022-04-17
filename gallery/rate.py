# Open this file with jeroenvantilburg.nl/ppg or any python environment
import matplotlib.pyplot as plt # do not modify; required by ppg
import numpy as np

# Data points with individual y-errors
x = [0, 22.5, 45, 67.5, 90 ]
y = [12.48, 10.73, 7.55, 2.01, 0.95 ]
yerr = [0.22, 0.19, 0.15, 0.05, 0.05]

# Create a numpy array of 100 entries with expected dependence
x_theory = np.linspace(0, 90, 100)
y_theory = y[0] * np.power(np.cos(x_theory/180*np.pi),2)

# Create the plot
fig, ax = plt.subplots()
ax.plot(x_theory, y_theory, label=r"theory ($\propto\cos^2\theta$)")
ax.errorbar(x, y, xerr=10, yerr=yerr, fmt='o', color='black', label="Measurements")
ax.legend(loc='upper right');

# Set the axis
ax.set_xlabel(r"$\theta$ ($^\circ$)", loc='right', fontsize=16)
ax.set_ylabel("Rate (mHz)", loc='top', fontsize=16)
ax.set_xlim([-1, 100])

# Show the major and minor grid lines
ax.minorticks_on()
ax.grid(which='major', color="grey", alpha=1, lw=0.5)
ax.grid(which='minor', color="grey", alpha=0.5, lw=0.4)

# Remove upper and right axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

plt.show() # last line; do not modify; required by ppg

