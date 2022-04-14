import numpy as np
import matplotlib.pyplot as plt
from math import *

def planckCurve(lam, T, I):
  h = 6.6261e-34
  c = 2.9979e8
  k = 1.38065e-23
  x = lam*1e-9 # lambda in nm
  return I*c**2/(lam**5 * (exp(h*c/(x*k*T))-1)) # in 10-4 W/m2
planck = np.vectorize(planckCurve)

# Create a numpy array of 500 entries
x = np.linspace(100, 2500, 500)

# Create the plot
fig, ax = plt.subplots()
ax.plot(x, planck(x,4000,110), color = 'grey', linestyle = 'dashdot', label="lamp 1")
ax.plot(x, planck(x,3170,403), color = 'orange', linestyle = 'dashed', label="lamp 2")
ax.plot(x, planck(x,2790,541), color = 'mediumblue', label="lamp 3")
ax.legend(loc='upper right', framealpha=1)

# Set the axis
ax.set_xlabel("$\lambda$ (nm)", loc='right', fontsize=12)
ax.set_ylabel("Intensiteit ($10^{-4}$ W m$^{-2}$) / nm", loc='top', fontsize=12)
ax.set_xlim([0, 2500])
ax.set_ylim([0, 450])
ax.set_aspect(3)

# Show the major and minor grid lines
ax.minorticks_on()
ax.grid(which='major', color="grey", alpha=1, lw=0.5)
ax.grid(which='minor', color="grey", alpha=1, lw=0.5)
import matplotlib.ticker as ticker
ax.yaxis.set_minor_locator(ticker.MultipleLocator(25))

# Remove upper and right axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

plt.show()
