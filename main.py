#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import logging
from lorenz_physics import LorenzPhysics
from anomaly_detector import AnomalyDetector
from knn_classifier import KNNClassifier

logging.basicConfig(
                    level=logging.INFO, 
                    filename='log.log', 
                    filemode = 'a',
                    format ='%(asctime)s | %(levelname)-8s | %(message)s', 
                    datefmt='%H:%M:%S',
                    force=True
                    )
print('logging configured')
logger = logging.getLogger(__name__)

def save_config(threshold, velocity_threshold, sigma, rho, beta):
    '''Save the detection threshold and reference parameters to config.json.'''
    config = {
        'Threshold': threshold,
        'Velocity_threshold': velocity_threshold,
        'Parameters': [sigma, rho, beta]
            }
        
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

def load_config():
    '''Load the detection threshold and reference parameters from config.json.'''
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config['Threshold'], config['Velocity_threshold'], config['Parameters']



def run_simulation():
    '''Run the full anomaly detection and classification pipeline.

    Loads or computes a reference trajectory and threshold, runs
    diagnostic sampling, and classifies any detected anomalies
    using KNN on the SPD manifold.'''
    detector = AnomalyDetector()
    if os.path.exists("config.json"):
        threshold_value, velocity_threshold, reference_parameters = load_config()
        reference_model = LorenzPhysics(reference_parameters[0], 
                                        reference_parameters[1], 
                                        reference_parameters[2])
        reference_trajectory = reference_model.path()
    else:  
        sigma, rho, beta = detector.monitor.get_average_lorenz_parameters(100) 
        model = LorenzPhysics(sigma, rho, beta)
        reference_trajectory = model.path()
        threshold_value = detector.threshold_value(reference_trajectory, 100)
        velocity_threshold = detector.velocity_threshold(100)
        save_config(threshold_value, velocity_threshold, sigma, rho, beta)
     
    matrices = detector.diagnostic(threshold_value, velocity_threshold, reference_trajectory, 200)
    classification = []
    classifier = KNNClassifier()
    for matrix in matrices:
        result = classifier.classify(matrix, 5)
        classification.append(result)
        logger.warning(f'Fault classified as: {result}')
run_simulation()