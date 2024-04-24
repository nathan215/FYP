import numpy as np
import pandas as pd
import math

# Constants
A= 2
n = 1.6   # Path-loss exponent
Z = -60 # Shadowing effect

# Function to calculate RSSI based on the path-loss model
def calculate_rssi(x, y):
    d = math.sqrt(x**2 + y**2)  # Euclidean distance from the origin
    if d == 0:  # Avoid log(0) error
        return A + Z
    RSSI = 2 - 10 * n * math.log10(d) + Z
    return RSSI

# Generate all points 5 meters apart from each other
x_range = range(-75, 76,5)  # From -75 to 75
y_range = range(-100, 101,10) # From -100 to 100

# List to store data
data = []

# Generate RSSI for each (x, y) point
for x in x_range:
    for y in y_range:
        rssi = calculate_rssi(x, y)
        data.append([x, y, rssi])

# Create a DataFrame
df = pd.DataFrame(data, columns=['x', 'y', 'rssi'])

# Save to CSV
df.to_csv('path_loss_rssi_data.csv', index=False)

print("CSV file generated successfully.")