import pandas as pd
import numpy as np
from math import log2

class Node:
    def __init__(self, col=None, val=None, results=None, tb=None, fb=None):
        self.col = col
        self.val = val
        self.results = results
        self.tb = tb
        self.fb = fb

def load_data(file_path):
    data = pd.read_csv(file_path, delimiter='\t')
    return data

def entropy(data):
    results = data['Class'].value_counts(normalize=True)
    entropy = sum([-p * log2(p) for p in results])
    return entropy

def split_data(data, column):
    split_data = {}
    unique_vals = data[column].unique()
    for val in unique_vals:
        split_data[val] = data[data[column] == val].reset_index(drop=True)
    return split_data

def build_tree(data):
    if len(data) == 0:
        return Node()
    current_score = entropy(data)
    best_gain = 0.0
    best_criteria = None
    best_sets = None
    columns = data.columns[:-1]
    for col in columns:
        sets = split_data(data, col)
        gain = current_score
        for key in sets:
            sub_set = sets[key]
            p = len(sub_set) / len(data)
            gain -= p * entropy(sub_set)
        if gain > best_gain and len(sets) > 1:
            best_gain = gain
            best_criteria = col
            best_sets = sets
    if best_gain > 0:
        true_branch = build_tree(best_sets[best_sets.keys()[0]])
        false_branch = build_tree(best_sets[best_sets.keys()[1]])
        return Node(col=best_criteria, tb=true_branch, fb=false_branch)
    else:
        return Node(results=data['Class'].value_counts().to_dict())

def classify(observation, tree):
    if tree.results != None:
        return list(tree.results.keys())[0]
    else:
        v = observation[tree.col]
        branch = None
        if isinstance(v, int) or isinstance(v, float):
            if v >= tree.val:
                branch = tree.tb
            else:
                branch = tree.fb
        else:
            if v == tree.val:
                branch = tree.tb
            else:
                branch = tree.fb
        return classify(observation, branch)

def test_accuracy(test_data, tree):
    test_data['Predicted'] = test_data.apply(classify, axis=1, args=(tree,))
    accuracy = sum(test_data['Class'] == test_data['Predicted']) / len(test_data)
    return accuracy

data = load_data('tennis.txt')
tree = build_tree(data)
accuracy = test_accuracy(data, tree)
print("Decision Tree:\n", tree, "\n\nTraining Set Accuracy: {:.2%}".format(accuracy))
