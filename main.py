#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from lorenz_physics import LorenzPhysics
from anomaly_detector import AnomalyDetector

def save_config(threshold, sigma, rho, beta):
    config = {
        'Threshold': threshold,
        'Parameters': [sigma, rho, beta]
            }
        
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config['Threshold'], config['Parameters']

detector = AnomalyDetector()

if os.path.exists("config.json"):
    
    sigma, rho, beta = detector.monitor.get_average_lorenz_parameters(100)
    
    model = LorenzPhysics(sigma, rho, beta)
    reference_trajectory = model.path()
    
    threshold_value = load_config()[0]
    detector.diagnostic(threshold_value, reference_trajectory, 200)
    
else:
    sigma, rho, beta = detector.monitor.get_average_lorenz_parameters(100)
    
    model = LorenzPhysics(sigma, rho, beta)
    reference_trajectory = model.path()
    
    threshold_value = detector.threshold_value(reference_trajectory, 100)
    save_config(threshold_value, sigma, rho, beta)
    detector.diagnostic(threshold_value, reference_trajectory, 200)
     