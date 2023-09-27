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
    slope, intercept, _, _, _ = linregress(log_distances, rssi_values)
    n = -slope / 10
    C = intercept
    return n, C  # returns n, C

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
    rssi_values = np.array([-60, -70, -80, -90,-100])
    distances = np.array([1, 10, 50, 100,1000])

    n, C = compute_parameters_linear(rssi_values, distances)
    print(f"N: {n}, C: {C}")

    plot_curve(distances, rssi_values, n, C)

    new_rssi = -75
    estimated_distance = rssi_to_distance(new_rssi, n, C)
    print(f"Estimated Distance for RSSI {new_rssi} dBm: {estimated_distance} meters")

if __name__ == '__main__':
    example_usage()