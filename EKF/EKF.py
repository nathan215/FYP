from scipy.optimize import minimize
import numpy as np
from scipy.optimize import minimize

# Define the path-loss model
def calculate_rssi(d, Z0=-41, n=3):
    return Z0 - 10 * n * np.log10(d)

def calculate_rssi_distance(rssi, P0=-41, n=3, d0=1):
    distance = d0 * (10 ** ((P0 - rssi) / (10 * n)))
    return distance

def partial_derivative(func, var=0, point=[]):
    args = point[:]
    def wraps(x):
        args[var] = x
        return func(*args)
    return wraps

def calculate_fim(L, Pk, sigma_sq):
    """
    Calculate the Fisher Information Matrix based on the signal power and its derivatives.
    L: State vector (x, y, z) of the LoRa node.
    Pk: Received signal power (RSSI) values.
    sigma_sq: Variance of the measurement noise.
    """
    FIM = np.zeros((3, 3))
    for i in range(3):  # x, y, z
        for j in range(3):  # x, y, z
            partial_u = partial_derivative(lambda L: calculate_rssi(L[i]), i)
            partial_v = partial_derivative(lambda L: calculate_rssi(L[j]), j)
            FIM[i, j] = np.sum(partial_u * partial_v / sigma_sq)
    return FIM

def calculate_jacobian(x_uav, y_uav, x_node, y_node):
    """
    Calculate the Jacobian matrix of the measurement function with respect to the node's position.
    
    Args:
    x_uav, y_uav: Coordinates of the UAV.
    x_node, y_node: Estimated coordinates of the LoRa node.
    
    Returns:
    Jacobian matrix H.
    """
    dx = x_node - x_uav
    dy = y_node - y_uav
    d = np.sqrt(dx**2 + dy**2)
    
    H = np.array([[dx / d, dy / d]])
    return H

def ekf_predict(x_est, P_est, Q, dt):
    # State transition matrix for a stationary target (LoRa node)
    Phi = np.eye(len(x_est))  # Assuming no movement, so identity matrix
    
    # Predicted state estimate
    x_pred = Phi @ x_est  # For stationary target, this is just x_est
    
    # Predicted estimate covariance
    P_pred = Phi @ P_est @ Phi.T + Q
    
    return x_pred, P_pred

def ekf_update(x_pred, P_pred, Z, R, dt):
    # Measurement function h(x) - Convert state estimate to predicted measurement
    # Placeholder: Assuming calculate_rssi_distance() gives distance (and thus RSSI) based on state
    H = calculate_jacobian(x_pred)  # Jacobian of h(x) at x_pred
    Z_pred = calculate_rssi_distance(x_pred)  # Predicted measurement based on x_pred
    
    # Innovation or measurement residual
    y = Z - Z_pred
    
    # Innovation (or residual) covariance
    S = H @ P_pred @ H.T + R
    
    # Optimal Kalman gain
    K = P_pred @ H.T @ np.linalg.inv(S)
    
    # Updated state estimate
    x_est = x_pred + K @ y
    
    # Updated estimate covariance
    P_est = (np.eye(len(x_est)) - K @ H) @ P_pred
    
    return x_est, P_est

def ekf_process(x_est, P_est, Z, Q, R, dt):
    # Prediction step
    x_pred, P_pred = ekf_predict(x_est, P_est, Q, dt)
    
    # Update step
    x_est, P_est = ekf_update(x_pred, P_pred, Z, R, dt)
    
    return x_est, P_est

def simulate_uav_flight_and_localization():
    results = []  # To store results of each trial

    for trial in range(num_trials):
        # Reset EKF state and covariance
        x_est = x0
        P_est = p0
        
        # Simulate UAV flight and measurements over the total_time
        # Assuming fixed steps, for simplification
        dt = 10  # Time step between measurements, in seconds
        for t in np.arange(0, total_time, dt):
            # Simulate UAV position change (Placeholder)
            alpha_change = np.radians(9)  # Change in azimuth angle
            
            # Simulate measurement (Placeholder for actual RSSI measurement)
            Z = np.random.normal(x_est, scale=np.sqrt(Q.diagonal()))
            
            # Update EKF based on simulated measurement
            x_est, P_est = ekf_update(x_est, P_est, Z, dt)
        
        # Store final estimated position for this trial
        results.append(x_est)
    
    return np.array(results)


# UAV flight and simulation parameters
total_time = 2540  # Total simulation time in seconds
phi_max = np.radians(15)  # Maximum pitch angle change in radians
alpha_max = np.radians(15)  # Maximum azimuth angle change in radians
Hmin = 0  # Minimum flight height

# EKF parameters
x0 = np.array([100, 100, 100])  # Initial state estimate
p0 = 100000 * np.eye(3)  # Initial state error covariance matrix
Q = 36 * np.eye(3)  # Process noise covariance matrix (variance = 36 for each element)
num_trials = 100  # Number of Monte Carlo experiments


# Run simulation
results = simulate_uav_flight_and_localization()
# Example: Calculate mean and standard deviation of the estimated positions
mean_position = np.mean(results, axis=0)
std_position = np.std(results, axis=0)

print("Mean Estimated Position:", mean_position)
print("Standard Deviation of Estimated Position:", std_position)
