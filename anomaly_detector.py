#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np
from system_monitor import SystemMonitor
from lorenz_physics import LorenzPhysics

class AnomalyDetector():
    def __init__(self):
        self.monitor = SystemMonitor()
    
    def covariance_matrix(self, trajectory):
        trajectory = np.array(trajectory)
        trajectory = trajectory.T
        return np.cov(trajectory)
    
    def frobenius_norm(self, matrix1, matrix2):
        matrix = matrix1 - matrix2
        return np.linalg.norm(matrix, ord='fro')
    
    def threshold_value(self,reference_trajectory, samples):
        sample_list = []
        matrix2 = self.covariance_matrix(reference_trajectory)
        for i in range(samples):
            sigma, rho, beta = self.monitor.get_lorenz_parameters()
            m1 = LorenzPhysics(sigma, rho, beta)
            trajectory1 = m1.path()
            matrix1 = self.covariance_matrix(trajectory1)
            frobenius_difference = self.frobenius_norm(matrix1, matrix2)
            sample_list.append(frobenius_difference)
        return np.mean(sample_list) + 3 * np.std(sample_list)
    
    def diagnostic(self, threshold, reference_trajectory, samples):
        matrix2 = self.covariance_matrix(reference_trajectory)
        for i in range(samples):
            sigma, rho, beta = self.monitor.get_lorenz_parameters()
            m1 = LorenzPhysics(sigma, rho, beta)
            trajectory = m1.path()
            matrix1 = self.covariance_matrix(trajectory)
            current_frobenius_norm = self.frobenius_norm(matrix1, matrix2)
            
            if current_frobenius_norm > threshold:
                print('Possible Anomaly Detected')
            else:
                if (i + 1) % 5 == 0:
                    print(f'Current Divergence: {current_frobenius_norm} and no anomalies. {threshold}')
            time.sleep(0.5)