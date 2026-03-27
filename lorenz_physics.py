#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
            
            dx = self.sigma * (self.y - self.x)
            dy = self.x *  (self.rho - self.z) - self.y
            dz = (self.x * self.y) - (self.beta * self.z)
            
            self.x = self.x + (dx * self.dt)
            self.y = self.y + (dy * self.dt)
            self.z = self.z + (dz * self.dt)
            
            self.trajectory.append((self.x, self.y, self.z))
            
        return self.trajectory
    
    def reset(self):
        
        self.trajectory = []
            
        self.x = self.x0
        self.y = self.y0
        self.z = self.z0
        
        return self.trajectory