import pandas as pd
import numpy as np
from scipy.stats import linregress

base_dir = "DroneSAR/data/esu/"
# List of y-values corresponding to the file names
y_values = [0, 5, 10, 30, 50, 70, 100]
# Initialize an empty list to store the data from all files
compiled_data = []

def compute_parameters_linear(df):
    distances = np.sqrt(df['x']**2 + df['y']**2)
    distances = np.where(distances == 0, 1e-4, distances)
    log_distances = np.log10(distances)
    slope, intercept, r_value, p_value, stderr = linregress(log_distances, df['rssi'])
    n = -slope / 10
    C = intercept
    return n, C, stderr

# Function to process each file
def process_file(y):
    file_path = f"{base_dir}data_{y}.xlsx"
    data_raw = pd.read_excel(file_path, header=None)
    data_raw.columns = ['pktId', 'sequence', 'label_rssi', 'rssi', 'label_snr', 'snr']
    data_clean = data_raw[pd.to_numeric(data_raw['rssi'], errors='coerce').notnull()].copy()
    num_rows_clean = len(data_clean)
    x_values_clean = np.linspace(-75, 75, num_rows_clean)
    data_clean.loc[:, 'x'] = x_values_clean 
    data_clean.loc[:, 'y'] = y

    # copy a reflect the y-axis and add add to the data
    if y != 0:
        data_clean_reflect = data_clean.copy()
        data_clean_reflect.loc[:, 'y'] = -data_clean_reflect['y']
        data_clean = pd.concat([data_clean, data_clean_reflect], ignore_index=True)

    return data_clean[['x', 'y', 'rssi']]

# Process each file and compile the data
for y in y_values:
    compiled_data.append(process_file(y))

# Concatenate all the dataframes into a single dataframe
final_compiled_data = pd.concat(compiled_data, ignore_index=True)
n, C, stderr = compute_parameters_linear(final_compiled_data)
print(f"Estimated n: {n}, Estimated C: {C}, Standard Error: {stderr}")
# Export the final dataframe to a CSV file in the current working directory
csv_output_path = f"{base_dir}compiled_data.csv"
final_compiled_data.to_csv(csv_output_path, index=False)

print(f"Data compiled successfully. CSV file created at: {csv_output_path}")


final_compiled_data['log_distance'] = np.log10(np.sqrt(final_compiled_data['x']**2 + final_compiled_data['y']**2))
final_compiled_data['theoretical_rssi'] = C - 10 * n * final_compiled_data['log_distance']
final_compiled_data['noise'] = final_compiled_data['rssi'] - final_compiled_data['theoretical_rssi']
noise_std = final_compiled_data['noise'].std()

print(f"The variance of the Gaussian noise is: {noise_std:.4f}")

import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial
import numpy as np
# Preparing data
distances =  np.sqrt(final_compiled_data['x']**2 + final_compiled_data['y']**2)
rssis = final_compiled_data['rssi']

# Fit a polynomial (2nd degree for simplicity and resemblance to exponential decay)
p = Polynomial.fit(distances, rssis, 2)

# Generate a sequence of distances for plotting the fit curve
x_fit = np.linspace(distances.min(), distances.max(), 500)
y_fit = p(x_fit)

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(distances, rssis, s=10, alpha=0.5, label='Data Points')  # smaller dots with s=10 and partial transparency
plt.plot(x_fit, y_fit, 'r', label='Fit Curve, Z0= -63.55, n= 1.51')
plt.xlabel('Distance')
plt.ylabel('RSSI')
plt.title('RSSI vs Distance')
plt.legend()
plt.grid(True)
plt.show()