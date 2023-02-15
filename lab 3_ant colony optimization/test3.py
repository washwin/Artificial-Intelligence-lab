import numpy as np
import sys
import math
import random

file = open(str(sys.argv[1]), "r")
typeOfDistance = str(file.readline())
numberOfCities = int(file.readline())
numberOfAnts = numberOfCities

for i in range(numberOfCities):
    coordinates = file.readline()

if typeOfDistance=="euclidean":
    alpha = 0.75
    beta = 12.5

if typeOfDistance=="noneuclidean":
    alpha = 10
    beta = 20

rho = 0.25
Q = 1.0

distanceMatrix = np.array(list(map(float,file.readline().split())))
for i in range(numberOfCities-1):
    line = list(map(float,file.readline().split()))
    distanceMatrix = np.vstack((distanceMatrix,line))

pheromoneMatrix = 100.00*np.ones((numberOfCities,numberOfCities))

def nextCity():
    remaining = []
    for i in range(numberOfCities):
        if i not in tour:
            remaining.append(i)
    eta = []
    for i in range(len(remaining)):
        tauAlpha = math.pow(pheromoneMatrix[tour[-1],remaining[i]], alpha)
        etaBeta = math.pow((1/pheromoneMatrix[tour[-1],remaining[i]]),beta)
        tauEta = tauAlpha*etaBeta
        eta.append(tauEta)

    sumOfEta = 0
    for i in eta:
        sum = sum + i

    ijProb = []
    for i in range(len(remaining)):
        ijProb.append(eta[i] / sumOfEta)

    temp = random.random
    i = 0
    x = ijProb[i]
    while True:
        if x > temp:
            return remaining[i]
        i = i + 1
        x = x + ijProb[i]

runs=0
minCost=-22
minTour=[]
while runs>30:
    runs += 1
    for ants in range(numberOfAnts):
        tour = []
        tour.append(0)          #starting city is 0
        while len(tour)!=numberOfCities:
            tour.append(nextCity)
        cost = 0.0
        for i in range(len(tour)-1):
            cost = cost + distanceMatrix[tour[i],tour[i+1]]
        
        if minCost == -22:
            minCost=cost
            minTour=tour

        if minCost>cost:
            minCost=cost
            minTour=tour
    Lk = 0
    for i in range(len(tour)-1):
        Lk = Lk + distanceMatrix[tour[i],tour[i+1]]

    for i in range(len(tour)-1):
        pheromoneMatrix[tour[i],tour[i+1]] *= rho
        pheromoneMatrix[tour[i+1],tour[i]] *= rho
        pheromoneMatrix[tour[i],tour[i+1]] += Q/Lk
        pheromoneMatrix[tour[i+1],tour[i]] += Q/Lk

    print(minTour)





