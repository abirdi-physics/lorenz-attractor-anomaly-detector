import numpy as np
import pickle
import os
from sklearn.ensemble import IsolationForest
from spd_manifold import SPDManifold

class IsolationForestClassifier:
    def __init__(self):
        self.spd_manifold = SPDManifold()
        self.forest = None
        self.frechet_mean = None
        if os.path.exists('forest.pkl'):
            with open('forest.pkl', 'rb') as f:
                self.forest = pickle.load(f)
        if os.path.exists('frechet_mean.npy'):
            self.frechet_mean = np.load('frechet_mean.npy')

    def train(self, matrices):
        frechet_mean = self.spd_manifold.frechet_mean(matrices)
        tangent_space_projection = []
        for i in range(len(matrices)):
            projection = self.spd_manifold.log_map_at(frechet_mean, matrices[i])
            tangent_vector = projection.flatten()
            tangent_space_projection.append(tangent_vector)

        self.forest = IsolationForest(contamination=0.1)
        self.forest.fit(tangent_space_projection)
        self.frechet_mean = frechet_mean
        with open ('forest.pkl', 'wb') as f:
            pickle.dump(self.forest, f)
        np.save('frechet_mean.npy', self.frechet_mean)

    def predict(self, matrix):
        projected_matrix = self.spd_manifold.log_map_at(self.frechet_mean, matrix)
        tangent_vector = projected_matrix.flatten()
        predict = self.forest.predict(tangent_vector.reshape(1, -1))
        if predict[0] == 1:
            return ('normal', None)
        return ('anomaflous', matrix)