import os, sys
sys.path.append(os.sep+os.path.join(*sys.path[0].split(os.sep)[1: -1]))
import numpy as np
from DroneSAR.env.map_esu_data import DroneRSSIEnv

def estimate_gradient(env, current_position, delta=10):
    x, y = current_position
    _, rssi_current, _, _ = env.step([x, y])  # Ensure this returns a scalar RSSI value

    # Estimating gradient with respect to x
    _, rssi_x, _, _ = env.step([x + delta, y])  # Ensure this returns a scalar RSSI value
    grad_x = (rssi_x - rssi_current) / delta

    # Estimating gradient with respect to y
    _, rssi_y, _, _ = env.step([x, y + delta])  # Ensure this returns a scalar RSSI value
    grad_y = (rssi_y - rssi_current) / delta

    print(f"X:{x}, Y: {y}, Current RSSI: {rssi_current}, RSSI x: {rssi_x}, RSSI y: {rssi_y}, Grad x: {grad_x}, Grad y: {grad_y}")
    return np.array([grad_x, grad_y])


def gradient_ascent(env, start_position, learning_rate=15, max_iterations=100):
    # Ensure that start_position is converted to a float array
    position = np.array(start_position, dtype=np.float64)

    for _ in range(max_iterations):
        grad = estimate_gradient(env, position)
        position -= learning_rate * grad  # Gradient ascent step
        env.render()
        # Optionally: Add any stopping criteria or position updates
    
    return position


# Example usage
env = DroneRSSIEnv(dataset_path='data/esu/compiled_data.csv')
start_position = (-20,50)  # Starting position
optimized_position = gradient_ascent(env, start_position)

print(f"Optimized Position: {optimized_position}")
