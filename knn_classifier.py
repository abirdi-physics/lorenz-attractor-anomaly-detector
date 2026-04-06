import json
import numpy as np
from spd_manifold import SPDManifold
from collections import Counter

class KNNClassifier():
    def __init__(self):
        with open ('covariance_map.json', 'r') as f:
            self.covariance_map = json.load(f)
        self.spd_manifold = SPDManifold()
        self.covariance_matrices = np.array(self.covariance_map['Atlas'])

    def classify(self, matrix, k):
        distance = []
        for i in range(len(self.covariance_matrices)):
            length = self.spd_manifold.distance(matrix, self.covariance_matrices[i])
            distance.append(length)
        k_nearest_indicies = np.argsort(distance)[:k]
        labels = []
        for l in k_nearest_indicies:
            neighbour_labels = self.covariance_map['Parameters'][l][3]
            labels.extend(neighbour_labels)
        if len(labels) == 0:
            return 'No Fault Detected'
        counts = Counter(labels)
        return counts.most_common(1)[0][0]