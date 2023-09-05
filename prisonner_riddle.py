import random as rd
import numpy as np
import matplotlib.pyplot as plt



def room(n):
    box = dict()
    L = np.arange(1, n+1)
    rd.shuffle(L)
    for i in range(1, n+1):
        box[i] = L[i-1]
    return box


def strategy(PRISONNERS, box):
    prisonner_safe = 0
    for prisonner in range(1, PRISONNERS+1):
        NOW = prisonner
        for attempt in range(PRISONNERS // 2):
            if box[NOW] == prisonner:
                prisonner_safe += 1
                break
            NOW = box[NOW]

    return prisonner_safe


def random(PRISONNERS, box):
    prisonner_safe = 0
    for prisonner in range(1, PRISONNERS+1):
        reste = np.arange(1, PRISONNERS+1)
        rd.shuffle(reste)
        for attempt in range(PRISONNERS // 2):
            if prisonner == box[reste[attempt]]:
                prisonner_safe += 1
                break
            
    return prisonner_safe

PRISONNERS = 100
x1 = []
x2 = []

for i in range(600):
    box = room(PRISONNERS)
    x1.append(strategy(PRISONNERS, box))
    x2.append(random(PRISONNERS, box))



plt.hist(x2, bins=PRISONNERS, density=True, width=.95, label='Random')
plt.hist(x1, bins=PRISONNERS, density=True, width=.85, label='With strategy')

plt.grid()
plt.xlabel('Prisonniers libres')
plt.ylabel('Probabilités')
plt.legend()
