import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import copy
import sys

dataset = pd.read_csv("tennis.txt", sep="\t")
X = dataset.iloc[:, 0:].values
datase = pd.read_csv('tennis.csv')
Y = datase.iloc[:, 1:].values

print(dataset.shape[0])
print(dataset.shape[1])
print(datase.shape[0])
print(datase.shape[1])