import numpy as np

def entropy(y):
    counts = np.bincount(y)
    probs = counts / len(y)
    return -np.sum([p * np.log2(p) for p in probs if p > 0])

def gini(y):
    counts = np.bincount(y)
    ps = counts / len(y)
    return 1 - np.sum(ps ** 2)

def information_gain(parent, left, right):
    weight_l = len(left) / len(parent)
    weight_r = len(right) / len(parent)
    return entropy(parent) - (weight_l * entropy(left) + weight_r * entropy(right))

def gini_gain(parent, left, right):
    weight_l = len(left) / len(parent)
    weight_r = len(right) / len(parent)
    return gini(parent) - (weight_l * gini(left) + weight_r * gini(right))   

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature   
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

class ID3DecisionTree:

    def __init__(self, max_depth=3, criterion='gini'):
        self.criterion = gini_gain if criterion == 'gini' else information_gain
        self.max_depth = max_depth
        self.root = None


    def fit(self, X, y):
        print(self.criterion.__name__)
        self.root = self.grow(X, y)
    
    def grow(self, X, y, depth=0):
        if len(set(y)) == 1 or depth >= self.max_depth: 
            return Node(value=np.bincount(y).argmax())  

        best_gain = -1
        best_feature, best_threshold = None, None
        best_left_mask, best_right_mask = None, None

        for feature in range(X.shape[1]):
            thresholds = np.unique(X[:, feature])
            if len(thresholds) > 10:
                thresholds = np.quantile(X[:, feature], [0.25, 0.5, 0.75])
            for t in thresholds:
                left_mask = X[:, feature] <= t   
                right_mask = ~left_mask

                if left_mask.sum() == 0 or right_mask.sum() == 0:
                    continue

                gain = self.criterion(y, y[left_mask], y[right_mask])

                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = t
                    best_left_mask = left_mask
                    best_right_mask = right_mask

        if best_gain < 1e-6 or best_feature is None:  
            return Node(value=np.bincount(y).argmax())

        left = self.grow(X[best_left_mask], y[best_left_mask], depth + 1)
        right = self.grow(X[best_right_mask], y[best_right_mask], depth + 1)
        return Node(feature=best_feature, threshold=best_threshold, left=left, right=right)

    def predict(self, X):
        return np.array([self._predict(inputs, self.root) for inputs in X])

    def _predict(self, inputs, node):
        if node.value is not None:
            return node.value
        if inputs[node.feature] <= node.threshold:
            return self._predict(inputs, node.left)
        else:
            return self._predict(inputs, node.right)
