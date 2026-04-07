#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy.linalg import eigh
import numpy as np

class SPDManifold:
    '''Riemannian geometry operations on the manifold of symmetric positive definite matrices.

    Provides logarithmic and exponential maps, geodesic distance,
    and Fréchet mean computation using the affine-invariant metric.'''
    def __init__(self):
        pass
    def _eigen_decompose(self, matrix):
        '''Compute the eigendecomposition of a symmetric matrix.
        :param matrix: symmetric matrix
        :return Tuple (eigenvalues, eigenvectors).'''
        return eigh(matrix)

    def log_map(self, matrix):
        '''Compute the matrix logarithm of an SPD matrix.
        :param matrix: symmetric matrix
        :return the symmetric matrix logarithm'''
        eigen_values, eigenvectors = self._eigen_decompose(matrix)
        return eigenvectors @ np.diag(np.log(eigen_values)) @ eigenvectors.T

    def log_map_at(self, base_point, target_point):
        '''Compute the logarithmic map at a base point on the SPD manifold.

        Maps target_point into the tangent space at base_point.

        :param base_point: The SPD matrix serving as the base point
        :param target_point: The SPD matrix to map into the tangent space.

        :return A symmetric matrix in the tangent space at base_point.
        '''
        base_eigen_values, base_eigenvectors = self._eigen_decompose(base_point)
        base_eigen_values_negative, base_eigen_values_positive = np.power(base_eigen_values, -0.5), np.power(base_eigen_values, 0.5)

        base_point_negative_sqrt = base_eigenvectors @ np.diag(base_eigen_values_negative) @ base_eigenvectors.T #Calculates base^(-1/2)
        base_point_positive_sqrt = base_eigenvectors @ np.diag(base_eigen_values_positive) @ base_eigenvectors.T #Calculates base^(1/2)

        inner_matrix = self.log_map(base_point_negative_sqrt @ target_point @ base_point_negative_sqrt)
        return base_point_positive_sqrt @ inner_matrix @ base_point_positive_sqrt

    def exp_map(self, matrix):
        '''Compute the matrix exponential of an SPD matrix.
                :param matrix: symmetric matrix
                :return the symmetric matrix exponential'''
        eigen_values, eigenvectors = self._eigen_decompose(matrix)
        return eigenvectors @ np.diag(np.exp(eigen_values)) @ eigenvectors.T

    def exp_map_at(self, base_point, tangent):
        '''Compute the exponential map at a base point on the SPD manifold.

        Maps a tangent vector back onto the manifold.
        :param base_point: The SPD matrix serving as the base point.
        :param tangent: A symmetric matrix in the tangent space at base_point.

        :return An SPD matrix on the manifold.'''
        base_eigen_values, base_eigenvectors = self._eigen_decompose(base_point)
        base_eigen_values_negative, base_eigen_values_positive = np.power(base_eigen_values, -0.5), np.power(base_eigen_values, 0.5)

        base_point_negative_sqrt = base_eigenvectors @ np.diag(base_eigen_values_negative) @ base_eigenvectors.T  # Calculates base^(-1/2)
        base_point_positive_sqrt = base_eigenvectors @ np.diag(base_eigen_values_positive) @ base_eigenvectors.T  # Calculates base^(1/2)

        inner_matrix = self.exp_map(base_point_negative_sqrt @ tangent @ base_point_negative_sqrt)
        return base_point_positive_sqrt @ inner_matrix @ base_point_positive_sqrt

    def distance(self, matrix1, matrix2):
        '''Compute the geodesic distance between two SPD matrices.
        :param matrix1: First SPD matrix.
        :param matrix2: Second SPD matrix.

        :return The affine-invariant Riemannian distance.
        '''
        matrix1_eigen_values, matrix1_eigenvectors = self._eigen_decompose(matrix1)
        matrix1_eigen_values = np.power(matrix1_eigen_values, -0.5)
        p1 = matrix1_eigenvectors @ np.diag(matrix1_eigen_values) @ matrix1_eigenvectors.T
        log = self.log_map(p1 @ matrix2 @ p1)
        return np.linalg.norm(log)

    def frechet_mean(self, data_points, max_iters=100):
        '''Compute the Fréchet mean of a set of SPD matrices.

        Iteratively refines the mean using log/exp maps until convergence.

        :param data_points: List of SPD matrices.
        :param max_iters: Maximum number of iterations.

        :return The Fréchet mean SPD matrix.s'''
        mu = data_points[0]

        for iterations in range(max_iters):
            tangent_matrices = [self.log_map_at(mu, p) for p in data_points]
            averaged_matrix = np.mean(tangent_matrices, axis=0)

            if np.linalg.norm(averaged_matrix) < 1e-9:
                break

            mu = self.exp_map_at(mu, averaged_matrix)
        return mu
