# Open this file with jeroenvantilburg.nl/ppg or any python environment
import matplotlib.pyplot as plt # do not modify; required by ppg
import numpy as np
from math import *

mu1 = 60
mu2 = 100
sigma1 = 8
sigma2 = 4

# Create a numpy array of 400 entries with a sinus
x = np.linspace(0, 150, 400)
y = 30/(np.sqrt(2*np.pi)*sigma1)*np.exp(-1*(x-mu1)**2/(2*sigma1**2)) \
    -30/(np.sqrt(2*np.pi)*sigma2)*np.exp(-1*(x-mu2)**2/(2*sigma2**2))
z = 75/(np.sqrt(2*np.pi)*sigma1)*np.exp(-1*(x-mu1)**2/(2*sigma1**2)) \
    -75/(np.sqrt(2*np.pi)*sigma2)*np.exp(-1*(x-mu2)**2/(2*sigma2**2))

fig, ax = plt.subplots()
ax.plot(x, -y,  color = 'black', linestyle = 'dashed', label="Bekende spoel N=400")
ax.plot(x, z, color = 'black', label="Onbekende spoel N=?   ")

ax.set_xlim([0, 150])
ax.set_ylim([-8.1, 5.1])
ax.set_xlabel("tijd (ms)", loc='right', fontsize=14)
ax.set_ylabel( "$U_{\mathrm{ind}}$ (V)", loc='top', fontsize=14)

# Show the minor ticks and the major grid
ax.minorticks_on()
ax.grid(which='major')
ax.grid(which='minor', alpha=1, lw=0.5)

ax.legend(loc='upper right', framealpha=1)

# Move bottom x-axis to centre, passing through (0,0)
ax.spines['bottom'].set_position('zero')
ax.spines['left'].set_position('zero')

# Eliminate upper and right axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')


plt.show() # last line; do not modify; required by ppg
