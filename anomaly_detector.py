#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import logging
from system_monitor import SystemMonitor
from lorenz_physics import LorenzPhysics

logger = logging.getLogger(__name__)

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
        m1 = LorenzPhysics(10, 28, 8/3)#these are dummy variables. 
        #We just want to instantiate the object, which get reset and properly assigned
        #in the loop below
        
        for i in range(samples):
            m1.reset()
            sigma, rho, beta = self.monitor.get_lorenz_parameters()
            
            m1.sigma = sigma
            m1.rho = rho
            m1.beta = beta
            
            trajectory1 = m1.path()
            matrix1 = self.covariance_matrix(trajectory1)
            frobenius_difference = self.frobenius_norm(matrix1, matrix2)
            sample_list.append(frobenius_difference)
            if (i + 1) % 5 == 0:
                print(f'Calculating Threshold. Step {i+1}/{samples}', end='\r')
        return np.mean(sample_list) + 3 * np.std(sample_list)
    
            
    def diagnostic(self, threshold, reference_trajectory, samples):
        matrix2 =self.covariance_matrix(reference_trajectory)
        m1 = LorenzPhysics(10, 28, 8/3) #these are dummy variables. 
        #We just want to instantiate the object, which get reset and properly assigned
        #in the loop below
        anomalous_matrices = []
        for i in range(samples):
            m1.reset()
            sigma, rho, beta = self.monitor.get_lorenz_parameters()
            
            m1.sigma = sigma
            m1.rho = rho
            m1.beta = beta
            
            trajectory = m1.path()
            matrix1 = self.covariance_matrix(trajectory)
            
            current_frobenius_norm = self.frobenius_norm(matrix1, matrix2)
            
            if current_frobenius_norm > threshold:
                logger.warning('Possible Anomaly')
                anomalous_matrices.append(matrix1)
            else:
                if (i + 1) % 5 == 0:
                    logger.info(f'Current Divergence: {current_frobenius_norm} and no anomalies. Threshold Value: {threshold}')
        return anomalous_matrices