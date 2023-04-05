import pandas as pd
import math
import copy
import sys

dataset = pd.read_csv(sys.argv[1], sep="\t")
X = dataset.iloc[:, 0:].values
f = open(sys.argv[1], "r")
attribute = f.readline().split('\t')
gain_dict = dict()

i=0
x=len(attribute)-1
while i < x:
    gain_dict[attribute[i]] = 0
    i=i+1
    

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
   
    pure = -1
    l=len(data[0])
    idx = l - 1
    entropy = 0
    yes = 0
    no = 0
    for i in rows:
        if data[i][idx] == 'yes':
            yes += 1
        else:
            no += 1
    s=yes+no
    x = yes/s
    y = no/s
    if x != 0 and y != 0:
        x1=math.log2(x)
        y1=math.log2(y)
        entropy = -1 * (x*x1 + y*y1)
    if x == 1:
        pure = 1
    if y == 1:
        pure = 0
    return entropy, pure

print_dict = dict()
def findMaxGain(data, rows, columns):
    maxGain = 0
    retidx = -1
    entropy, pure = findEntropy(data, rows)
    if entropy == 0:
        return maxGain, retidx, pure

    for j in columns:
        mydict = dict()
        for i in rows:
            key = data[i][j]
            if key in mydict:
                mydict[key] = mydict[key] + 1
                
            else:
                mydict[key] = 1
                
        gain = entropy
        attribute_val = []
        for key in mydict:
            yes = 0
            no = 0
            attribute_val.append(key)
            for k1 in rows:
                if data[k1][j] == key:
                    if data[k1][-1] == 'yes':
                        yes+= 1
                    else:
                        no+= 1
            s=yes+no            
            x = yes/s
            y = no/s
            if x != 0 and y != 0:
                x1=math.log2(x)
                y1=math.log2(y)
                z=mydict[key]
                gain = gain + ((x*x1 + y*y1)*z)/dataset.shape[0]
        if gain > maxGain:
            maxGain = gain
            retidx = j
        print_dict[attribute[j]] = attribute_val

    return maxGain, retidx, pure


def buildTree(data, rows, columns):

    maxGain, idx, pure = findMaxGain(X, rows, columns)
    root = Node()
    root.children = list()
    
    if maxGain == 0:
        if pure == 0:
            root.n1 = 'no'
        else:
            root.n1 = 'yes'
        return root

    root.n1 = attribute[idx]
    mydict = dict()
    for i in rows:
        key = data[i][idx]
        if key in mydict:
            mydict[key] = mydict[key] + 1
        else:
            mydict[key] = 1


    newcolumns = copy.copy(columns)
    newcolumns.remove(idx)
    for key in mydict:
        newrows = list()
        k=0
        for i in rows:
            if data[i][idx] == key:
                newrows.insert(k,i)
                k=k+1
            
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
        j=0
        while j<n:
            traverse(root.children[j])
            j=j+1



def calculate():
    rows = list()
    i=0
    while i<dataset.shape[0]:
        rows.append(i)
        i=i+1

    columns = list()
    i=0
    while i<dataset.shape[1]-1:
        columns.insert(i,i)
        i=i+1

    root = buildTree(X, rows, columns)
    root.n2 = "Start"
    traverse(root)


calculate()

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