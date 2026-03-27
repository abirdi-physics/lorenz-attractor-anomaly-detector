#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from system_monitor import SystemMonitor
from lorenz_physics import LorenzPhysics



model = LorenzPhysics(10, 28, 8/3)
reference_trajectory = model.path()

live_model = SystemMonitor()
threshold_value = live_model.threshold_value(reference_trajectory, 100)
live_model.diagnostic(threshold_value, reference_trajectory, 300)

