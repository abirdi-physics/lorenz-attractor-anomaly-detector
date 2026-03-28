#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import numpy as np
import time
from lorenz_physics import LorenzPhysics

class SystemMonitor:
    def __init__(self):
        pass
    
    def get_lorenz_parameters(self):
        
        cpu_load = psutil.cpu_percent(interval=0.5)
        ram_load = psutil.virtual_memory().percent
        cpu_current_clock, cpu_min_clock, cpu_max_clock = psutil.cpu_freq()
        
        sigma = (cpu_load / 100) * (15 - 5) + 5
        rho = (ram_load/100) * (40 - 20) + 20
        beta = (cpu_current_clock/ cpu_max_clock) * (4 - 1.5) + 1.5
        
        return sigma, rho, beta
    
    def get_average_lorenz_parameters(self, loops):
        parameters = []
        for i in range(loops):
            parameters.append(self.get_lorenz_parameters())
            time.sleep(0.5)
        parameters = np.array(parameters)
        return np.mean(parameters, axis=0)
    
    def distance(self, point1, point2): #Finds distance between points
        
        return np.sqrt((point1[0] - point2[0])**2
                       + (point1[1] - point2[1]) ** 2
                       + (point1[2] - point2[2]) ** 2) 

    def mean_divergence(self, trajectory1, trajectory2):
        distances = []
        for i in range(len(trajectory1)):
            point1 = trajectory1[i]
            point2 = trajectory2[i]
            distances.append(self.distance(point1, point2))
            
        return np.mean(distances)
    
    def covariant_matrix(self, trajectory):
        trajectory = np.array(trajectory)
        trajectory = trajectory.T
        return np.cov(trajectory)
    
    def frobenius_norm(self, matrix1, matrix2):
        matrix = matrix1 - matrix2
        return np.linalg.norm(matrix, ord='fro')
    
    def threshold_value(self,reference_trajectory, samples):
        sample_list = []
        for i in range(samples):
            sigma, rho, beta = self.get_lorenz_parameters()
            m1 = LorenzPhysics(sigma, rho, beta)
            trajectory1 = m1.path()
            matrix1 = self.covariant_matrix(trajectory1)
            matrix2 = self.covariant_matrix(reference_trajectory)
            frobenius_difference = self.frobenius_norm(matrix1, matrix2)
            sample_list.append(frobenius_difference)
        return np.mean(sample_list) + 3 * np.std(sample_list)
    
    def diagnostic(self, threshold_value, reference_trajectory, samples):
        matrix2 = self.covariant_matrix(reference_trajectory)
        for i in range(samples):
            sigma, rho, beta = self.get_lorenz_parameters()
            m1 = LorenzPhysics(sigma, rho, beta)
            trajectory = m1.path()
            matrix1 = self.covariant_matrix(trajectory)
            current_frobenius_norm = self.frobenius_norm(matrix1, matrix2)
            
            if current_frobenius_norm > threshold_value:
                print('Possible Anomaly Detected')
            elif current_frobenius_norm <= threshold_value:
                if (i + 1) % 5 == 0:
                    print(f'Current Divergence: {current_frobenius_norm} and no anomalies. {threshold_value}')
            time.sleep(0.5)