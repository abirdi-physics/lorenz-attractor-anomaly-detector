#!/usr/bin/env python3
# -*- coding: utf-8 -*-
TRANSIENT_STEPS = 100
class LorenzPhysics:
    '''Simulates the Lorenz attractor using RK4 integration.

    Generates 3D trajectories from the Lorenz system of differential
    equations, parameterised by sigma, rho, and beta.
    '''
    def __init__(self, sigma, rho, beta, steps=1100, x=1, y=1, z=1):
        '''Initialises the Lorenz system.
        :param:
            sigma: Prandtl number controlling the rate of convective overturning.
            rho: Rayleigh number controlling the temperature difference.
            beta: Geometric factor of the convection cell.
            steps: Number of integration steps.
            x: Initial x position.
            y: Initial y position.
            z: Initial z position.'''
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
        '''Integrate the Lorenz system and return the trajectory.

        Uses 4th-order Runge-Kutta. The first TRANSIENT_STEPS points
        are discarded to remove transient behaviour.

        :return
            List of (x, y, z) tuples along the attractor.
        '''
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
        '''Compute the Lorenz system derivatives at a given point.
        :param x: The x position of the Lorenz system.
        :param y: The y position of the Lorenz system.
        :param z: The z position of the Lorenz system.

        :return
            tuple of derivatives (dx, dy, dz
            '''
        dx = self.sigma * (y - x)
        dy = x *  (self.rho - z) - y
        dz = (x * y) - (self.beta * z)
        return dx, dy, dz
    
    def reset(self):
        '''reset the system state and trajectory to inital conditions.
        '''
        self.trajectory = []
        
        self.x = self.x0
        self.y = self.y0
        self.z = self.z0