import numpy as np
import json
from itertools import product
from lorenz_physics import LorenzPhysics
from anomaly_detector import AnomalyDetector


def save_config(atlas, parameters):
    '''Save atlas of matrices and Lorenz parameters to JSON file called covariance_map.json
    '''
    config = {
        'Atlas': atlas,
        'Parameters': parameters
    }

    with open('covariance_map.json', 'w') as f:
        json.dump(config, f, indent=4)

def parameter_sweep(sigma_range, rho_range, beta_range):
    '''Generate a covariance atlas by sweeping Lorenz parameter space.

    Simulates trajectories for all combinations of sigma, rho, and beta,
    computes their covariance matrices, and assigns fault labels based
    on parameter thresholds.
    
    :param sigma_range  Array of sigma values to sweep:
    :param rho_range Array of rho values to sweep:
    :param beta_range Array of beta values to sweep:

    :return Tuple (atlas, parameters) where atlas is a list of covariance
        matrices and parameters is a list of [sigma, rho, beta, faults]:
    '''
    atlas = []
    parameters = []
    monitor = AnomalyDetector()
    total = len(sigma_range) * len(rho_range) * len(beta_range)
    counter = 0
    for s, r, b in product(sigma_range, rho_range, beta_range):
        fault = []
        if s >= 10:
            fault.append('CPU fault')
        if r >= 33:
            fault.append('RAM pressure')
        if b <= 2.75:
            fault.append('CPU thermal pressure')
        butterfly = LorenzPhysics(s, r, b)
        trajectory = butterfly.path()
        covariance_matrix = monitor.covariance_matrix(trajectory)
        covariance_matrix = covariance_matrix.tolist()
        atlas.append(covariance_matrix)
        parameters.append([s.item(), r.item(), b.item(), fault])
        counter += 1

        if counter % 5 == 0:
            print(f'Performing parameter sweep. Step {counter}/{total}', end='\r')
    return atlas, parameters

if __name__ == '__main__':
    sigma_range  = np.linspace(5, 15, 10)
    rho_range = np.linspace(26, 40, 10)
    beta_range = np.linspace(1.5, 4, 10)

    atlas, parameters = parameter_sweep(sigma_range, rho_range, beta_range)
    save_config(atlas, parameters)
