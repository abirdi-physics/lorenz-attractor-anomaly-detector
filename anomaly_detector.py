#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import logging
from system_monitor import SystemMonitor
from lorenz_physics import LorenzPhysics
from spd_manifold import SPDManifold

logger = logging.getLogger(__name__)

class AnomalyDetector():
    ''' Detects anomalies by comparing covariance matrices of different Lorenz trajectories.

    Samples live system metrics and simulates Lorenz trajectories. Then flags anomalies
    when the geodesic distance between two covariance matrices exceeds a statistically derived threshold.
    '''
    def __init__(self):
        self.monitor = SystemMonitor()
        self.spd_manifold = SPDManifold()

    def covariance_matrix(self, trajectory):
        '''Computes the covariance matrix of a trajectory.

        :param trajectory list of tuples (x, y, z):
        :return 3 x 3 numpy array (covariance matrix):
        '''
        trajectory = np.array(trajectory)
        trajectory = trajectory.T
        return np.cov(trajectory)

    def threshold_value(self,reference_trajectory, samples):
        '''Calculates the threshold for anomaly detection.

        Samples live Lorenz trajectories and calculates the mean + 3 standard deviations
        of the geodesic distance to the reference covariance matrix.

        :param baseline trajectory to compare against samples to calculate threshold:
        :return threshold value:'''
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
            geodesic_distance = self.spd_manifold.distance(matrix1, matrix2)
            sample_list.append(geodesic_distance)
            if (i + 1) % 5 == 0:
                print(f'Calculating Threshold. Step {i+1}/{samples}')
        return np.mean(sample_list) + 3 * np.std(sample_list)
    
            
    def diagnostic(self, threshold, reference_trajectory, samples):
        '''Run anomaly detection over a number of samples.

        Compares each sampled covariance matrix against the reference
        using geodesic distance and collects those exceeding the threshold.

        :param threshold: The anomaly threshold value.
            reference_trajectory: Baseline trajectory to compare against.
            samples: Number of diagnostic samples to evaluate:

        :return list of covariance matrices that exceed the threshold:'''
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

            current_distance = self.spd_manifold.distance(matrix1, matrix2)
            
            if current_distance > threshold:
                logger.warning('Possible Anomaly')
                anomalous_matrices.append(matrix1)
            else:
                if (i + 1) % 5 == 0:
                    logger.info(f'Current Divergence: {current_distance} and no anomalies. Threshold Value: {threshold}')
        return anomalous_matrices