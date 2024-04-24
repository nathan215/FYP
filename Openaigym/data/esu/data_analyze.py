import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

# Define the log-distance path loss model function
def path_loss_model(distance, n, A):
    distance = np.maximum(distance, 1e-10)  # Avoid log of zero
    return -10 * n * np.log10(distance) + A

# Load the original data
data = pd.read_csv('data/esu/compiled_data.csv')
data['distance'] = np.sqrt(data['x']**2 + data['y']**2)
distances = data['distance'].values
rssis = data['rssi'].values

# Fit the path loss model to get n and A
params, _ = curve_fit(path_loss_model, distances, rssis)
n_estimated, A_estimated = params

# Create a scaled-down grid of points
x_values = np.arange(-50, 51, 5)  # Reduced range and increased step size
y_values = np.arange(-50, 51, 5)  # Reduced range and increased step size
xx, yy = np.meshgrid(x_values, y_values)
xx_flat = xx.flatten()
yy_flat = yy.flatten()

# Calculate distances for the grid
distances_new = np.sqrt(xx_flat**2 + yy_flat**2)

# Handle the special case for (x, y) = (0, 0)
zero_index = np.where((xx_flat == 0) & (yy_flat == 0))
special_rssi = path_loss_model(1, n_estimated, A_estimated)  # Avoid log of zero

# Calculate expected RSSI using the path loss model
expected_rssi_new = path_loss_model(distances_new, n_estimated, A_estimated)
expected_rssi_new[zero_index] = special_rssi  # Apply the special case

# Analyze the error distribution in original data
original_errors = rssis - path_loss_model(distances, n_estimated, A_estimated)
error_std = np.std(original_errors)

# Set up a Gaussian Process for spatial correlation
gp_kernel = RBF(length_scale=0.2)
gpr = GaussianProcessRegressor(kernel=gp_kernel, alpha=error_std**2)
gpr.fit(np.vstack([data['x'], data['y']]).T, original_errors)

# Generate errors for the new dataset
predicted_errors = gpr.sample_y(np.vstack([xx_flat, yy_flat]).T, random_state=42).flatten()

# Combine expected RSSI and errors
final_rssi_new = expected_rssi_new + predicted_errors

# Create the new dataset
new_dataset = pd.DataFrame({
    'x': xx_flat,
    'y': yy_flat,
    'rssi': final_rssi_new
})

# Save the new dataset to a CSV file
new_dataset.to_csv('generated_dataset.csv', index=False)

print("New dataset generated and saved as 'generated_dataset.csv'")

# plot (x, y, rssi) data
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# ax.scatter(data['x'], data['y'], data['rssi'], c='b', marker='o')
ax.scatter(new_dataset['x'], new_dataset['y'], new_dataset['rssi'], c='r', marker='^')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('RSSI (dBm)')
plt.show()







