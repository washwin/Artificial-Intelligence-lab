import pandas as pd
import math
import copy
import sys

dataset = pd.read_csv(sys.argv[1], sep="\t")
X = dataset.iloc[:, 0:].values



f = open(sys.argv[1], "r")
attribute = f.readline().split('\t')
gain_dict = {}
for i in range(0,len(attribute)-1):
    gain_dict[attribute[i]] = 0

print_dict = {}


class Node(object):
    def __init__(self):
        self.n1 = None
        self.n2 = None
        self.children = None


def predict(instance, tree):
    attribute = list(tree.keys())[0]
    if instance[attribute] in tree[attribute]:
        result = tree[attribute][instance[attribute]]
        if isinstance(result, dict):
            return predict(instance, result)
        else:
            return result
    else:
        return "No"
    

def findEntropy(data, rows):
    yes = 0
    no = 0
    pure = -1
    idx = len(data[0]) - 1
    entropy = 0
    for i in rows:
        if data[i][idx] == 'yes':
            yes = yes + 1
        else:
            no = no + 1

    x = yes/(yes+no)
    y = no/(yes+no)
    if x != 0 and y != 0:
        entropy = -1 * (x*math.log2(x) + y*math.log2(y))
    if x == 1:
        pure = 1
    if y == 1:
        pure = 0
    return entropy, pure


def findMaxGain(data, rows, columns):
    maxGain = 0
    retidx = -1
    entropy, pure = findEntropy(data, rows)
    if entropy == 0:
        return maxGain, retidx, pure

    for j in columns:
        mydict = {}
        for i in rows:
            key = data[i][j]
            if key not in mydict:
                mydict[key] = 1
            else:
                mydict[key] = mydict[key] + 1
        gain = entropy
        for i in rows:
            key = data[i][j]
            if key not in gain_dict:
                gain_dict[key] = 0
        attribute_val = []
        for key in mydict:
            yes = 0
            no = 0
            attribute_val.append(key)
            for k in rows:
                if data[k][j] == key:
                    if data[k][-1] == 'yes':
                        yes = yes + 1
                    else:
                        no = no + 1
            x = yes/(yes+no)
            y = no/(yes+no)
            if x != 0 and y != 0:
                gain += (mydict[key] * (x*math.log2(x) + y*math.log2(y)))/dataset.shape[0]
                gain_dict[key] = gain
        if gain > maxGain:
            maxGain = gain
            retidx = j
        print_dict[attribute[j]] = attribute_val

    return maxGain, retidx, pure


def buildTree(data, rows, columns):

    maxGain, idx, pure = findMaxGain(X, rows, columns)
    root = Node()
    root.children = []
    if maxGain == 0:
        if pure == 1:
            root.n1 = 'yes'
        else:
            root.n1 = 'no'
        return root

    root.n1 = attribute[idx]
    mydict = {}
    for i in rows:
        key = data[i][idx]
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
        temp = buildTree(data, newrows, newcolumns)
        temp.n2 = key
        root.children.append(temp)
    return root


def traverse(root):
    if root.n2 == "Start":
        print(root.n1)
    else:
        print(root.n2)
        print(root.n1)

    n = len(root.children)
    if n > 0:
        for i in range(0, n):
            traverse(root.children[i])


def calculate():
    rows = []
    i=0
    while i<dataset.shape[0]:
        rows.append(i)
        i=i+1

    columns = []
    i=0
    while i<dataset.shape[1]-1:
        columns.append(i)
        i=i+1

    root = buildTree(X, rows, columns)
    root.n2 = "Start"
    traverse(root)



calculate()
# print(gain_dict)

def getAccuracy(tree, columns):
    Correct=0
    Incorrect=0
    predictions = []
    for instance in dataset:
        prediction = predict(instance, tree)
        if(instance[columns] == prediction):
            Correct+=1
        else:
            Incorrect+=1
        predictions.append(prediction)

    print("Correct = ", Correct,"\n", "Incorrect = ",Incorrect,"\n")
    print("Accuracy = ",100*Correct/(Correct+Incorrect),"%")