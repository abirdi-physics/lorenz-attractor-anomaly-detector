import json
import numpy as np
from spd_manifold import SPDManifold
from collections import Counter

class KNNClassifier():
    '''K-nearest neighbours classifier on the SPD manifold.

    Classifies anomalous covariance matrices by finding the closest
    entries in a pre-computed atlas using geodesic distance, then
    returning the most common fault label among the k nearest neighbours.
    '''
    def __init__(self):
        '''Load covariance matrix atlas from covariance_map.json'''
        with open ('covariance_map.json', 'r') as f:
            self.covariance_map = json.load(f)
        self.spd_manifold = SPDManifold()
        self.covariance_matrices = np.array(self.covariance_map['Atlas'])

    def classify(self, matrix, k):
        '''Classify an anomalous covariance matrix by fault type.

        :param matrix: Covariance matrix to classify
        :param k: The number of nearest neighbours to consider

        :return String label of the most common fault, or 'No Fault Detected'''
        distance = []
        for i in range(len(self.covariance_matrices)):
            length = self.spd_manifold.distance(matrix, self.covariance_matrices[i])
            distance.append(length)
        k_nearest_indicies = np.argsort(distance)[:k]
        labels = []
        for l in k_nearest_indicies:
            neighbour_labels = self.covariance_map['Parameters'][int(l)][3]
            labels.append(neighbour_labels)
        if len(labels) == 0:
            return 'No Fault Detected'
        counts = Counter(labels)
        return counts.most_common(1)[0][0]