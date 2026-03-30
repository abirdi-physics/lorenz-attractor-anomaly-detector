#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lorenz_physics import LorenzPhysics
from anomaly_detector import AnomalyDetector


detector = AnomalyDetector()
sigma, rho, beta = detector.monitor.get_average_lorenz_parameters(100)

model = LorenzPhysics(sigma, rho, beta)
reference_trajectory = model.path()

threshold_value = detector.threshold_value(reference_trajectory, 100)
detector.diagnostic(threshold_value, reference_trajectory, 300)