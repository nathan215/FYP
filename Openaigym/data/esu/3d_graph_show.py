from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import griddata

# Load the data
data = pd.read_csv('path_loss_rssi_data.csv')

# Create a grid of points to interpolate RSSI values
grid_x, grid_y = np.mgrid[min(data['x']):max(data['x']):100j, min(data['y']):max(data['y']):100j]

# Interpolate the RSSI values
x = data['x'].values
y = data['y'].values

rssi_values = data['rssi'].values
grid_rssi = griddata( ( x,y), rssi_values, (grid_x, grid_y), method='cubic')

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(grid_x, grid_y, grid_rssi, cmap='viridis', linewidth=0, antialiased=False, alpha = 0.3)

# Add a color bar which maps values to colors.
cbar = fig.colorbar(surf, shrink=0.5, aspect=5)
cbar.set_label('RSSI')

# Set labels and title
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('RSSI')
ax.set_title('3D RSSI Distribution')

plt.show()
fig.savefig('3d_pathloss_rssi.png')

exit()
plt.figure(figsize=(10, 8))

contour = plt.contourf(grid_x, grid_y, grid_rssi, cmap='viridis', alpha=0.75)
cbar = plt.colorbar(contour)
cbar.set_label('RSSI')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('2D RSSI Distribution (Contour Plot)')
plt.grid(True)

contour_plot_path = 'data/esu/2d_rssi_contour_plot.png'
plt.savefig(contour_plot_path)
plt.show(), contour_plot_path