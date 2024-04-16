import matplotlib.pyplot as plt
import numpy as np
from shared_state import find_combined_data, current_drone_location

def draw_path():
    if find_combined_data:
        structured_array = np.array([(d['x'], d['y']) for d in find_combined_data], dtype=[('x', float), ('y', float)])
        
        x_coords = structured_array['x']
        y_coords = structured_array['y']
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='blue', label='Path')
        
        if current_drone_location:
            current_x, current_y = current_drone_location
            plt.plot(current_x, current_y, marker='*', color='red', markersize=15, label='Current Location')
        
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Drone Path')
        plt.legend()
        plt.grid(True)
        
        # Save the plot to a file instead of displaying it
        plt.savefig('drone_path.png')
        plt.close()  # Close the figure to free up memory

