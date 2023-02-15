import numpy as np
import sys
import math
import random

file = open(str(sys.argv[1]), "r")
typeOfDistance = str(file.readline())

numberOfCities = int(file.readline())

numberOfAnts = 100

for i in range(numberOfCities):
    coordinates = file.readline()

alpha = 0.75  
beta = 12.5

if typeOfDistance == "noneuclidean":
    alpha = 10
    beta = 20

rho = 0.25
Q = 1.0

distanceMatrix = np.array(list(map(float,file.readline().split())))
for i in range(numberOfCities):
    line = list(map(float,file.readline().split()))
    distanceMatrix = np.vstack((distanceMatrix,line))

# pheromoneMatrix = 100.0*np.ones((numberOfCities,numberOfCities))
pheromoneMatrix = []
N = numberOfCities
for i in range(N):
    temp = []
    for j in range(N):
        temp.append(1/N*N*N) 
    pheromoneMatrix.append(temp)
    
    
    
    

def nextCity(tour, numberOfCities, distanceMatrix, pheromoneMatrix, alpha, beta):
    remaining = []
    for i in range(numberOfCities):
        if i not in tour:
            remaining.append(i)
    
    eta = []
    len1 = len(remaining)
    for i in range(len1):
        tauAlpha = math.pow(pheromoneMatrix[tour[-1]][remaining[i]], alpha)
        etaBeta = math.pow((1/distanceMatrix[tour[-1],remaining[i]]),beta)
        tauEta = tauAlpha*etaBeta
        eta.append(tauEta)

    sumOfEta = 0
    for i in eta:
        sumOfEta = sumOfEta + i
    
    ijProb = []
    for i in range(len1):
        ijProb.append(eta[i] / sumOfEta)
    # print(ijProb)
    y = math.fsum(ijProb)
    z = len(ijProb)
    # print(x)
    # exit()
    tempVar = random.uniform(0,1)
    i = 0
    x = ijProb[i]
    while True:
        if x > tempVar:
            return remaining[i]
        i = i + 1
        x = x + ijProb[i]


runs = 0
minCost = -22
minTour = []
for i in range(numberOfAnts):
    minTour.append(i)
    
while runs < 30:
    runs = runs + 1
    newPheromoneMatrix = pheromoneMatrix.copy()

    tour = []
    for ants in range(numberOfAnts):
        tour.append(22)          #starting city is 0
        while len(tour) != numberOfCities:
            tour.append(nextCity(tour, numberOfCities, distanceMatrix, pheromoneMatrix, alpha, beta))
        cost = 0
        len2 = len(tour)-1
        for i in range(len2):
            cost = cost + distanceMatrix[tour[i],tour[i+1]]
    
        if minCost == -22:
            minCost = cost
            minTour = tour

        if minCost > cost:
            minCost = cost
            minTour = tour
    Lk = 0
    for i in range(len2):
        Lk = Lk + distanceMatrix[tour[i],tour[i+1]]

    for i in range(len2):
        newPheromoneMatrix[tour[i+1]][tour[i]] *= rho
        newPheromoneMatrix[tour[i]][tour[i+1]] += Q/Lk
        newPheromoneMatrix[tour[i]][tour[i+1]] *= rho
        newPheromoneMatrix[tour[i+1]][tour[i]] += Q/Lk
       
    pheromoneMatrix = newPheromoneMatrix
    
    best = 0
    for i in range(len2):
        best = best + distanceMatrix[minTour[i],minTour[i+1]]
    print(best)
    
    for i in range(numberOfCities):
        if i == numberOfCities:
            print(minTour[i])
            break
        print(minTour[i], end = ' ')
    print("\n------------------------------------------x-------------------------------------------\n")
