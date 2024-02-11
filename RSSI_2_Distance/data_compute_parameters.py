import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import linregress
import matplotlib.pyplot as plt

def model_function(distance, n, C):
    return C - 10 * n * np.log10(distance)

# def compute_parameters(distances, rssi_values):
#     popt, _ = curve_fit(model_function, distances, rssi_values)
#     return popt[0], popt[1]  # returns n, C

def compute_parameters_linear(rssi_values, distances):
    log_distances = np.log10(distances)
    slope, intercept, _, _, stderr = linregress(log_distances, rssi_values)
    n = -slope / 10
    C = intercept
    return n, C, stderr  # Include standard error as a measure of noise

def rssi_to_distance(rssi, n, C):
    return 10 ** ((C - rssi) / (10 * n))

def plot_curve(distances, rssi_values, n, C):
   
    plt.figure(figsize=(10, 5))
    
    # Define specific x-axis ticks
    x_ticks = [1, 10, 100, 1000]
    
    # Plotting Fitted line for log(distance) vs. RSSI
    plt.scatter(distances, rssi_values, c='red', label='Original Data')
    log_distances = np.log10(distances)
    fitted_rssi = C - 10 * n * log_distances
    plt.plot(distances, fitted_rssi, 'b-', label='Fitted Line')
    plt.xscale('log')
    plt.xticks(ticks=x_ticks, labels=x_ticks)  # Manually set the ticks on x-axis
    plt.xlabel('Distance (m) [Log Scale]')
    plt.ylabel('RSSI (dBm)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage:
def example_usage():
    rssi_values = np.array([-92,-78,-87,-80])
    x = np.array([200,90,50,60])
    y = np.array([200,90,200,60])
    z = np.array([2,14,44,48])
    distances = np.sqrt(x**2 + y**2 + z**2)
    n, C = compute_parameters_linear(rssi_values, distances)
    print(f"N: {n}, C: {C}")

    plot_curve(distances, rssi_values, n, C)

    new_rssi = -40
    estimated_distance = rssi_to_distance(new_rssi, n, C)
    print(f"Estimated Distance for RSSI {new_rssi} dBm: {estimated_distance} meters")

# i want to caculate n,c for "D:\FYP\PHD_Task\DroneSAR\data\esu\compiled_data.csv"
import pandas as pd
df = pd.read_csv("D:\FYP\PHD_Task\DroneSAR\data\esu\compiled_data.csv")
df['rssi'] = df['rssi'].astype(float)
df['distance'] = np.sqrt(df['x']**2 + df['y']**2 + 5**2)

# Compute parameters
n, C, noise_estimate = compute_parameters_linear(df['rssi'], df['distance'])
print(f"N: {n}, C: {C}, Noise Estimate: {noise_estimate}")