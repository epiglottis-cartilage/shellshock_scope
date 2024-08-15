import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

file = np.loadtxt('data.csv',delimiter=',')
x = file[:,0]
x.sort()
y = file[:,1]

def f(x,a,b,c):
    return a*x**2+b*x+c

plt.figure()
plt.plot(x,y)

popt,pcov = curve_fit(f, x, y)
plt.plot(x,f(x,*popt))
plt.show()

print(f'curve_fit: {popt[0]}x^2 + {popt[1]}x + {popt[2]}')