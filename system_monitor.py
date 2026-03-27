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
        
        cpu_load = psutil.cpu_percent(interval=None)
        ram_load = psutil.virtual_memory().percent
        cpu_current_clock, cpu_min_clock, cpu_max_clock = psutil.cpu_freq()
        
        sigma = (cpu_load / 100) * (15 - 5) + 5
        rho = (ram_load/100) * (40 - 20) + 20
        beta = (cpu_current_clock/ cpu_max_clock) * (4 - 1.5) + 1.5
        
        return sigma, rho, beta
    
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
    
    def threshold_value(self,reference_trajectory, samples):
        sample_list = []
        for i in range(samples):
            sigma, rho, beta = self.get_lorenz_parameters()
            m1 = LorenzPhysics(sigma, rho, beta)
            trajectory1 = m1.path()
            divergence = self.mean_divergence(trajectory1, reference_trajectory)
            sample_list.append(divergence)
        return np.mean(sample_list) + 3 * np.std(sample_list)
    
    def diagnostic(self, threshold_value, reference_trajectory, samples):
        for i in range(samples):
            sigma, rho, beta = self.get_lorenz_parameters()
            m1 = LorenzPhysics(sigma, rho, beta)
            trajectory = m1.path()
            current_divergence = self.mean_divergence(trajectory, reference_trajectory)
            if current_divergence > threshold_value:
                print('Possoble Anomaly Detected')
            elif current_divergence <= threshold_value:
                if (i + 1) % 5 == 0:
                    print(f'Current Divergence: {current_divergence} and no anomalies. {threshold_value}')
            time.sleep(0.5)