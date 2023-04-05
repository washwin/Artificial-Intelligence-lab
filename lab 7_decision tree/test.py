import pandas as pd
import numpy as np
import math
import copy

f = open("tennis.txt","r")
attribute = f.readline().split('\t')
gain_dict = {}
for i in range(0,len(attribute)-1):
    gain_dict[attribute[i]] = 0

class Node(object):
    def __init__(self):
        self.value = None
        self.decision = None
        self.childs = None
# print(df.iloc[1])
# print(len(df.iloc[1]))
# print(df.shape[0])  
# print(total_columns)
# print(df.iloc[:, idx])          #entire column
# print(df.iloc[1,3])               #that particular 
def log_2(a):
    if a==0:
        return 0
    else:
        return math.log2(a)


def calculateEntropy(data, total_rows):   
    entropy = 0
    yes = 0
    no = 0
    ans = -1
    for i in range(0,total_rows):
        if data.iloc[i,-1] == "yes":
            yes += 1
        else:
            no += 1
    a = yes/(yes+no)
    b = no/(yes+no)
    if a!=0 and b!=0: 
        entropy = -1 * (a*log_2(a) + b*log_2(b))
    if a==1:
        ans = 1
    if b==1:
        ans = 0
    # print(entropy)
    return entropy, ans


def calculateGain(df, total_rows, total_columns):
    max_gain = 0
    idx = -1
    entropy, ans = calculateEntropy(df, total_rows) 
    if entropy==0:
        return max_gain, idx, ans
    
    for j in range(0, total_columns):
        mydict = {}
        gain = entropy
        for i in range(0, total_rows):
            key = df.iloc[i,j]
            if key not in mydict:
                mydict[key] = 1
            else:
                mydict[key] += 1
    
        for key in mydict:
            yes = 0
            no = 0
            for k in range(0, total_rows):
                if df.iloc[k,j] == key:
                    if df.iloc[k,-1] == "yes":
                        yes += 1
                    else:
                        no += 1
            a = yes/(yes+no)
            b = no/(yes+no)
            if a!=0 and b!=0:
                gain += (mydict[key] * (a*log_2(a) + b*log_2(b)))/total_rows               
        if gain>max_gain:
            max_gain=gain
            idx = j
        gain_dict[attribute[j]] = gain
    return max_gain, idx, ans

def buildTree(data, rows, columns):

    maxGain, idx, ans = calculateGain(df, rows, columns)
    root = Node()
    root.childs = []
    # print(maxGain
    #
    # )
    if maxGain == 0:
        if ans == 1:
            root.value = 'yes'
        else:
            root.value = 'no'
        return root

    root.value = attribute[idx]
    mydict = {}
    for i in range(0,rows):
        key = data.iloc[i,idx]
        if key not in mydict:
            mydict[key] = 1
        else:
            mydict[key] += 1

    newcolumns = copy.deepcopy(columns)
    newcolumns.remove(idx)
    for key in mydict:
        newrows = []
        for i in rows:
            if data[i][idx] == key:
                newrows.append(i)
        # print(newrows)
        temp = buildTree(data, newrows, newcolumns)
        temp.decision = key
        root.childs.append(temp)
    return root


def traverse(root):
    print(root.decision)
    print(root.value)

    n = len(root.childs)
    if n > 0:
        for i in range(0, n):
            traverse(root.childs[i])


def calculate():
    df = pd.read_csv("tennis.txt", sep='\t')
    rows = df.shape[0]
    columns = df.shape[1] - 1
    root = buildTree(df, rows, columns)
    root.decision = 'Start'
    traverse(root)


calculate()   
    


