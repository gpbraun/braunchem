import numpy as np
import matplotlib.pyplot as plt

KW = 1e-14

KB = 2e-5
CB = 4e-4
VB = 25

CA = 1e-3

VMAX = 20

PH = np.linspace(0, 14, 100)


def volume(x):
    delta = KW / x - x
    alpha = KB / (KW / x + KB)

    return VB * (CB * alpha - delta) / (CA + delta)


xs = []
ys = []

for p in PH:
    v = volume(10 ** (-p))
    if v > 0 and v < VMAX:
        xs.append(v)
        ys.append(p)

## PLOTING

plt.plot(xs, ys)
plt.show()
