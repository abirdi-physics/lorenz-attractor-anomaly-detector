#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from system_monitor import SystemMonitor
from lorenz_physics import LorenzPhysics


live_model = SystemMonitor()
sigma, rho, beta = live_model.get_average_lorenz_parameters(100)

model = LorenzPhysics(sigma, rho, beta)
reference_trajectory  =model.path()


threshold_value = live_model.threshold_value(reference_trajectory, 100)
live_model.diagnostic(threshold_value, reference_trajectory, 300)

