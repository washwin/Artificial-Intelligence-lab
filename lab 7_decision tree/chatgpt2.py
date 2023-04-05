import pandas as pd
import numpy as np
import math

class DecisionTree:
    def __init__(self):
        self.root = None
        
    def fit(self, X, y):
        self.root = self.build_tree(X, y)
        
    def build_tree(self, X, y):
        # Stopping criterion: all instances belong to the same class
        if y.nunique() == 1:
            return y.iloc[0]
        
        # Stopping criterion: no more attributes to split on
        if X.shape[1] == 1:
            return y.value_counts().idxmax()
        
        # Select the attribute with the highest information gain
        split_attr = self.select_attribute(X, y)
        tree = {split_attr: {}}
        
        # Split the dataset based on the selected attribute
        for attr_val, subset in X.groupby(split_attr):
            subset_y = y.loc[subset.index]
            tree[split_attr][attr_val] = self.build_tree(subset.drop(columns=[split_attr]), subset_y)
            
        return tree
        
    def select_attribute(self, X, y):
        # Calculate the information gain of each attribute
        ent_D = self.entropy(y)
        gains = []
        for col in X.columns:
            ent_A = 0
            for attr_val, subset in X.groupby(col):
                subset_y = y.loc[subset.index]
                ent_A += (subset_y.shape[0] / y.shape[0]) * self.entropy(subset_y)
            gains.append((col, ent_D - ent_A))
        
        # Select the attribute with the highest information gain
        return max(gains, key=lambda x: x[1])[0]
        
    def entropy(self, y):
        # Calculate the entropy of a class distribution
        count_y = y.value_counts()
        p_y = count_y / len(y)
        return -(p_y * np.log2(p_y)).sum()
        
    def predict(self, X):
        return X.apply(self.predict_instance, axis=1)
        
    def predict_instance(self, instance):
        node = self.root
        while type(node) == dict:
            attr_val = instance[node.keys()][0]
            node = node[node.keys()][attr_val]
        return node
        
    def accuracy(self, X, y):
        y_pred = self.predict(X)
        return (y_pred == y).mean()

# Read the tab-delimited dataset file
df = pd.read_csv("tennis.txt", sep="\t")

# Split the dataset into the feature matrix and the target vector
X = df.drop(columns=["classification"])
