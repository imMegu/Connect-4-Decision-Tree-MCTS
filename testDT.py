import pandas as pd
import numpy as np
from ID3 import ID3DecisionTree

# Load and prepare iris data
def load_iris_data(filename):
    df = pd.read_csv(filename)
    
    class_map = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
    df['class'] = df['class'].map(class_map)
    
    feature_cols = ['sepallength', 'sepalwidth', 'petallength', 'petalwidth']
    
    X = df[feature_cols].values
    y = df['class'].values
    
    return X, y

def load_c4_dataset(path, size=None):
    # Load the CSV file
    df = pd.read_csv(path)

    X = df.drop(columns=['move']).values  # shape: (n_samples, 42)
    y = df['move'].values                 # shape: (n_samples,)
    
    return X[:size], y[:size]

def train_test_split(X, y, test_size=0.3, random_state=None):
    if random_state:
        np.random.seed(random_state)
    
    # Shuffle indices
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    
    # Calculate split point
    split = int((1 - test_size) * len(X))
    
    # Split data
    X_train = X[indices[:split]]
    X_test = X[indices[split:]]
    y_train = y[indices[:split]]
    y_test = y[indices[split:]]
    
    return X_train, X_test, y_train, y_test

def classification_report(y_true, y_pred, labels=None, target_names=None):

    if labels is None:
        labels = np.unique(np.concatenate((y_true, y_pred)))
    
    # Calculate metrics per class
    metrics = []
    for label in labels:
        true_pos = np.sum((y_true == label) & (y_pred == label))
        false_pos = np.sum((y_true != label) & (y_pred == label))
        false_neg = np.sum((y_true == label) & (y_pred != label))
        
        precision = true_pos / (true_pos + false_pos) if (true_pos + false_pos) > 0 else 0
        recall = true_pos / (true_pos + false_neg) if (true_pos + false_neg) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        support = np.sum(y_true == label)
        metrics.append((precision, recall, f1, support))

    max_name_len = max(len(str(name)) for name in (target_names or labels))
    header = f"{'':<{max_name_len}}  {'precision':>10}  {'recall':>10}  {'f1-score':>10}  {'support':>10}"
    report = [header]
    for i in labels:
        name = target_names[i] if target_names else str(label)
        p, r, f1, s = metrics[i]
        line = f"{name:<{max_name_len}}  {p:>10.2f}  {r:>10.2f}  {f1:>10.2f}  {s:>10}"
        report.append(line)

    report.extend([
        "\n",
        f"Accuracy: {np.mean(y_true == y_pred):.3f}"])

    return "\n".join(report)

if __name__ == "__main__":
    try:
        X, y = load_c4_dataset('dataset.csv', None)
        #X, y = load_iris_data('iris.csv')
        
        print(X.shape)
        print(y.shape)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        print(X_test)

        from sklearn.tree import DecisionTreeClassifier
        tree = DecisionTreeClassifier(max_depth=15, criterion='gini')
        tree.fit(X_train, y_train)
        y_pred = tree.predict(X_test)
        print("sklearn's ID3 classification report: \n")
        print(classification_report(y_test, y_pred, target_names=["0", "1", "2", "3", "4", "5", "6"]))

        tree = ID3DecisionTree(max_depth=15, criterion='gini')    
        tree.fit(X_train, y_train)
        y_pred = tree.predict(X_test)
        print("Our ID3's classification report: \n")
        print(classification_report(y_test, y_pred, target_names=["0", "1", "2", "3", "4", "5", "6"]))
    
    except Exception as e:
        print(f"Error: {e}")
