#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import numpy as np
import time


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
