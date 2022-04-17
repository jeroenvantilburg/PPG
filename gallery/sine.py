# Open this file with jeroenvantilburg.nl/ppg or any python environment
import matplotlib.pyplot as plt # do not modify; required by ppg
import numpy as np

x = np.linspace(0, 2.0 * np.pi, 100)
y = np.sin(x)

plt.figure()
plt.plot(x, y)
plt.show() # last line; do not modify; required by ppg
