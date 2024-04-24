import sys, os
sys.path.append(os.sep+os.path.join(*sys.path[0].split(os.sep)[1: -1]))
from bayes_opt import BayesianOptimization
import numpy as np
import math
import random

def does_line_intersect_circle(x1, y1, x2, y2, circle_radius=5):
    """
    Check if the line segment between (x1, y1) and (x2, y2) intersects a circle
    centered at the origin with the specified radius.
    """
    # Line segment direction vector
    dx, dy = x2 - x1, y2 - y1
    # Line segment length squared
    dr_squared = dx**2 + dy**2
    # Determinant
    D = x1*y2 - x2*y1
    # Discriminant
    discriminant = circle_radius**2 * dr_squared - D**2
    
    return discriminant >= 0

# Define the parameter bounds
def basic_bayesian(f, x_start, step=50,pbounds={'x': (-800, 800), 'y': (-800, 800)}, num_iter=50):
    
    def f_wrapper(x, y):
        return f([x, y])  # Assuming f expects a list [x, y]
    
    initial_points = [
        {'x': x_start[0], 'y': x_start[1]},
        {'x': x_start[0], 'y':x_start[1]-step},
        {'x': x_start[0]-step, 'y': x_start[1]-step}
    ]
    # Initialize the Bayesian optimizer
    optimizer = BayesianOptimization( f=f_wrapper, pbounds=pbounds
                                     , verbose=0, random_state=1,
                                       allow_duplicate_points= True)
    # Execute optimization
    for point in initial_points:
        optimizer.register(params=point, target=f_wrapper(**point))
    optimizer.maximize(init_points=0, n_iter=num_iter)

    all_points = []
    for res in optimizer.res:
        x = res['params']['x']
        y = res['params']['y']
        all_points.append([np.array([x, y]), res['target']])
    return optimizer.max, all_points


def objective_function(x, y, noise):
            path_loss_n = 1.6  # path-loss exponent
            path_loss_A = -60  # path-loss at reference distance
            d = np.sqrt((x - 0)**2 + (y - 0)**2)  # distance to the origin
            estimated_rssi = -10 * path_loss_n * math.log10(d) + path_loss_A + np.random.normal(0, noise)
            return estimated_rssi

def main():
    noise_levels = np.arange(0, 10, 0.5)
    sucess = {}
    record = {}
    # Loop over the noise levels
    for i in range(1, 10):
        x_start = np.random.randint(-500, 500, 2)

        for noise in noise_levels:
            f = lambda x, y: objective_function(x, y, noise)
            result, all_points = basic_bayesian(f, x_start)
            break
    # plot accuracy
    import matplotlib.pyplot as plt
    accuracy = [sucess[noise]/10 for noise in noise_levels]
    plt.plot(noise_levels, accuracy)
    plt.xlabel('Noise Level')
    plt.ylabel('Success Rate')
    plt.title('Success Rate vs. Noise Level')
    plt.show()
    efficiency = [np.mean(record[noise]) for noise in noise_levels]
    plt.plot(noise_levels, efficiency)
    plt.xlabel('Noise Level')
    plt.ylabel('Average Iteration')
    plt.title('Average Iteration vs. Noise Level')
    plt.show()

