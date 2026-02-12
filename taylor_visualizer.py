# function must be continuous and infinitely differentiable at all points.

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def f(x):
    f = np.sin(x)
    return f     # defining f(x) = sin(x). in principle, the code should work for other functions too, but not tested yet.

pt = float(input("approximate around: ")) 
ord = 0     # initial order of taylor polynomial

low_lim = pt - 3.14
up_lim = pt + 3.14
dx = 0.0001
x_arr = np.arange(low_lim,up_lim + dx, dx)
x_arr = np.unique(np.append(x_arr, pt))     # to ensure that pt is in the array
y_arr = np.sin(x_arr)

# now we take nth derivative at x = pt using finite difference method

def nth_der(x0, n):
    r = 0
    a = 0
    while r <= n:
        a = a + (math.comb(n, r)*(-1)**r*f(x0+(n-2*r)*dx))
        r += 1
    return a/(2*dx)**n     # blows up at 6th order derivative for sin x at x = 0

fig, (ax)= plt.subplots()
plt.subplots_adjust(bottom=0.2)

ax.grid()
ax.spines['left'].set_position(('data', pt))     # places vertical axis at x = pt
ax.spines['bottom'].set_position('zero')     # places horizontal axis at y = 0
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.plot(x_arr, y_arr, marker = None, color = 'black')
ax.plot(pt, f(pt), marker = 'o', color = 'blue')

# constructing taylor polynomial of order ord, about pt

def p(x, x0, n):
    k = 0
    b = 0
    while k <= n:
        b = b + ((nth_der(x0, k))*(x-x0)**k)/(math.factorial(k))
        k += 1
    return b

taylor_arr = p(x_arr, pt, ord)

taylor_line, = ax.plot(x_arr, taylor_arr, marker = None, color = 'blue')
ax.set_xlim (low_lim-0.2, up_lim+0.2)
ax.set_ylim (-1.2, 1.2)

slider = Slider(plt.axes([0.4, 0.1, 0.2, 0.01]), valmin=0, valmax=4, valinit= ord, valstep=1, label='Order ')
# at x = 1, 5th order taylor polynomial blows up and gets less accuurate than 4th order (why?), so valmax is set to 4 

def update(ord):
    ord = slider.val
    taylor_line.set_ydata(p(x_arr, pt, ord))
    fig.canvas.draw_idle()

slider.on_changed(update)

plt.show()