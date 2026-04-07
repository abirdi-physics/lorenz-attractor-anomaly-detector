#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import numpy as np


class SystemMonitor:
    '''Maps real-time system metrics to Lorenz attractor parameters.

    CPU load maps to sigma, RAM usage maps to rho, and CPU clock
    speed ratio maps to beta.'''
    def __init__(self):
        pass
    
    def get_lorenz_parameters(self):
        '''Sample current system metrics and return corresponding Lorenz parameters.

        :return
                Tuple (sigma, rho, beta) derived from CPU load, RAM usage,
            and CPU clock speed.'''
        
        cpu_load = psutil.cpu_percent(interval=0.1)
        ram_load = psutil.virtual_memory().percent
        cpu_current_clock, cpu_min_clock, cpu_max_clock = psutil.cpu_freq()
        
        sigma = (cpu_load / 100) * (15 - 5) + 5
        rho = (ram_load/100) * (40 - 26) + 26
        beta = (cpu_current_clock/ cpu_max_clock) * (4 - 1.5) + 1.5
        
        return sigma, rho, beta
    
    def get_average_lorenz_parameters(self, loops):
        '''Average Lorenz parameters over multiple samples.
        :param loops Number of samples to average over.:
        :return Array of mean (sigma, rho, beta) values.:
        '''
        parameters = []
        for i in range(loops):
            parameters.append(self.get_lorenz_parameters())
        parameters = np.array(parameters)
        return np.mean(parameters, axis=0)
