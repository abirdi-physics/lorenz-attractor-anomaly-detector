#!/usr/bin/env python3
# -*- coding: utf-8 -*-
TRANSIENT_STEPS = 100
class LorenzPhysics:
    def __init__(self, sigma, rho, beta, steps=1100, x=1, y=1, z=1):
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
        self.steps = steps
        self.dt = 0.001
        
        self.x = x
        self.y = y
        self.z = z
        
        self.x0 = x
        self.y0 = y
        self.z0 = z
        
        self.trajectory = []

        
    def path(self):
        for i in range(self.steps):
            
            k1 = self._lorenz_derivatives(self.x, self.y, self.z)
            
            k2 = self._lorenz_derivatives(self.x + self.dt/2 * k1[0], 
                                          self.y + self.dt/2 * k1[1], 
                                          self.z + self.dt/2 * k1[2])
            
            k3  = self._lorenz_derivatives(self.x + self.dt/2 * k2[0],
                                           self.y + self.dt/2 * k2[1],
                                           self.z + self.dt/2 * k2[2])
            
            k4 = self._lorenz_derivatives(self.x + self.dt * k3[0],
                                          self.y + self.dt * k3[1],
                                          self.z + self.dt * k3[2])
            
            self.x = self.x + self.dt/6 * (k1[0] + 2*k2[0] + 2*k3[0] + k4[0])
            self.y = self.y + self.dt/6 * (k1[1] + 2*k2[1] + 2*k3[1] + k4[1])
            self.z = self.z + self.dt/6 * (k1[2] + 2*k2[2] + 2*k3[2] + k4[2])
            
            self.trajectory.append((self.x, self.y, self.z))
            
        return self.trajectory[TRANSIENT_STEPS:]
    
    def _lorenz_derivatives(self, x, y, z):
        dx = self.sigma * (y - x)
        dy = x *  (self.rho - z) - y
        dz = (x * y) - (self.beta * z)
        return dx, dy, dz
    
    def reset(self):
        
        self.trajectory = []
            
        return self.trajectory