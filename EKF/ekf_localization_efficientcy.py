import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from scipy.spatial.distance import euclidean
from tqdm import tqdm
from numpy.linalg import pinv

# Constants
Z0, n, d0 = -41, 1.6, 1  # Path-loss model parameters
noise_level = 5  # Noise level (standard deviation of the noise)
import numpy as np

# Constants
Q = np.eye(3) * 36  # Process noise covariance matrix
R = np.eye(1) * 25  # Measurement noise variance, assuming noise level 5, squared

# Initial values
x0 = np.array([100, 100, 100]).reshape(-1, 1)  # Reshape to (3, 1) if necessary
P0 = np.eye(3) * 100000  # Initial state error covariance

def simulate_rssi(x, y, z, Z0=Z0, n=n, d0=d0):
    d = np.sqrt(x**2 + y**2 + z**2) or d0  # Avoid division by zero
    rssi = Z0 - 10 * n * np.log10(d / d0)
    return rssi

def jacobian_h(x_est):

    x, y, z = x_est.flatten()  # Make sure x_est is a flat array if it's not
    d = np.sqrt(x**2 + y**2 + z**2)
    hx = -10 * n * x / (d * np.log(10))
    hy = -10 * n * y / (d * np.log(10))
    hz = -10 * n * z / (d * np.log(10))
    H = np.array([[hx, hy, hz]])  # Shape (1, 3)
    return H

def prediction_step(x_est, P_est, Q):
    # Assuming state transition matrix Phi is identity because the target is stationary
    Phi = np.eye(3)  
    x_pred = Phi.dot(x_est)  # Dot product for matrix multiplication
    P_pred = Phi.dot(P_est).dot(Phi.T) + Q
    
    # Ensure x_pred is a column vector
    x_pred = x_pred.reshape(-1, 1)
    return x_pred, P_pred

def update_step(x_pred, P_pred, Z, R):
    
    x_pred = x_pred.reshape(-1, 1)  # Ensure x_pred is a column vector
    H = jacobian_h(x_pred)
    Z_pred = simulate_rssi(*x_pred)
    y = Z - Z_pred  # Innovation, ensure Z is appropriately shaped

    # If Z is a scalar, reshape y to be a column vector
    y = np.array([y]).reshape(-1, 1)  # Reshape y as a column vector if necessary

    S = H @ P_pred @ H.T + R  # Innovation covariance
    K = P_pred @ H.T @ np.linalg.inv(S)  # Kalman gain

    # Ensure K @ y is a valid operation by verifying dimensions
    x_est = x_pred + K @ y  # Updated state estimate, now should work as intended
    P_est = P_pred - K @ H @ P_pred  # Updated estimate covariance
    x_est = x_est.reshape(-1, 1)
    return x_est, P_est

# Generate random measurement points in space
def generate_measurement_points(num_points, measurement_range=100):
    points = np.random.uniform(-measurement_range, measurement_range, size=(num_points, 3))
    return points

# Simulate RSSI measurement
def simulate_real_rssi(x, y, z, noise_level=noise_level, Z0=Z0, n=n, d0=d0):
    d = np.sqrt(x**2 + y**2 + z**2) or d0  # Avoid division by zero
    rssi = Z0 - 10 * n * np.log10(d / d0) + np.random.normal(0, noise_level)
    return rssi

# MLE for position based on average of distance estimates
def mle_position(measurements, Z0=Z0, n=n, d0=d0):
    distances = d0 * (10 ** ((Z0 - measurements[:,3]) / (10 * n)))
    # Placeholder for position estimation; more sophisticated method needed for real application
    # This example averages x, y, z coordinates weighted by estimated distances
    weights = 1 / distances
    estimated_position = np.average(measurements[:, :3], axis=0, weights=weights)
    return estimated_position

def ekf_position(measurements, x0=x0, P0=P0, Q=Q, R=R):
    x_est, P_est = x0, P0
    for Z in measurements[:, 3]:  # Assuming last column is RSSI
        Z_vec = np.array([[Z]])  # Shape Z as 2D column vector
        
        # Prediction
        x_pred, P_pred = prediction_step(x_est, P_est, Q)
        
        # Update
        x_est, P_est = update_step(x_pred, P_pred, Z_vec, R)
        
        # Assertion removed as x_pred and x_est are now ensured to be correctly shaped
    return x_est.flatten()  # Or keep as is depending on how you want to use it

def l3m_mre_simple(measurements, Z0, alpha, R):
    # Assume measurements is a NumPy array of shape (N, 4) where columns are x, y, z, rssi
    
    N = measurements.shape[0]
    anchor_combinations = combinations(range(N), R)
    
    best_error = np.inf
    best_estimated_location = None
    
    for comb in anchor_combinations:
        selected_measurements = measurements[np.array(comb)]
        # Use a simplified direct estimation method for the selected measurements
        # Placeholder for direct position estimation, adjust as necessary
        # For demonstration, we simply take the mean position of selected anchors
        estimated_pos = np.mean(selected_measurements[:, :3], axis=0)
        
        # Calculate the total error for this combination
        total_error = 0
        for m in selected_measurements:
            d = euclidean(m[:3], estimated_pos)
            estimated_rssi = Z0 - 10 * alpha * np.log10(d)
            error = abs(m[3] - estimated_rssi)
            total_error += error
        
        # Update best estimate if this combination has lower error
        if total_error < best_error:
            best_error = total_error
            best_estimated_location = estimated_pos
    
    return np.array(best_estimated_location)

def l3m(measurements, Z0, alpha):
    """
    Estimates position from RSSI measurements using trilateration.
    
    Args:
    measurements: NumPy array of shape (N, 4), where each row is [x, y, z, rssi]
    Z0: RSSI at reference distance (1 meter)
    alpha: Path loss exponent
    
    Returns:
    Estimated position as a NumPy array [x, y, z]
    """
    # Extract coordinates and RSSI values
    coords = measurements[:, :3]  # x, y, z coordinates
    rssi_values = measurements[:, 3]  # RSSI values
    
    # Convert RSSI values to distances
    distances = 10 ** ((Z0 - rssi_values) / (10 * alpha))
    
    # Prepare matrices for trilateration
    A = np.zeros((len(coords), 3))
    b = np.zeros(len(coords))
    
    for i, (xi, yi, zi) in enumerate(coords):
        Ri_squared = distances[i] ** 2
        A[i] = [-2*xi, -2*yi, -2*zi]
        b[i] = Ri_squared - xi ** 2 - yi ** 2 - zi ** 2
    
    # Solve for position using least squares (pseudo-inverse)
    position = pinv(A).dot(b)
    
    return position

# Evaluate localization error for increasing number of measurement points
num_measurements = 20
ekf_errors = []
mle_errors = []
mew_errors = []
l3m_errors = []
true_position = np.array([0, 0, 0])

# Generate points once outside the loop
points = generate_measurement_points(num_measurements)
rssi_measurements = np.array([simulate_real_rssi(x, y, z) for x, y, z in points])

for num_points in tqdm(range(3, num_measurements + 1)):
    current_points = points[:num_points]  # Use a slice of points up to num_points
    current_rssi_measurements = rssi_measurements[:num_points]  # Use a slice of RSSI measurements up to num_points
    measurements = np.hstack((current_points, current_rssi_measurements[:, None]))
    
    mle_est = mle_position(measurements)
    ekf_est = ekf_position(measurements)  # Placeholder: replace with actual EKF implementation
    mre_est = l3m_mre_simple(measurements, Z0, 4, 3)
    l3m_est = l3m(measurements, Z0, 4)
    
    mle_errors.append(np.linalg.norm(mle_est - true_position))
    ekf_errors.append(np.linalg.norm(ekf_est - true_position))
    mew_errors.append(np.linalg.norm(mre_est - true_position))
    l3m_errors.append(np.linalg.norm(l3m_est - true_position))

# Plotting adjustments
plt.figure(figsize=(10, 6))
plt.plot(range(3, num_measurements + 1), mle_errors, label='MLE Error', marker='o')
plt.plot(range(3, num_measurements + 1), ekf_errors, label='EKF Error', linestyle='--', marker='x')
plt.plot(range(3, num_measurements + 1), mew_errors, label='MRE Error', linestyle='-.', marker='s')
plt.plot(range(3, num_measurements + 1), l3m_errors, label='L3M Error', linestyle=':', marker='d')
plt.xlabel('Number of Measurement Points')
plt.ylabel('Localization Error (units)')
plt.title('Localization Error vs. Number of Points')
plt.legend()
plt.grid(True)
plt.show()