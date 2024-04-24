import gym
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from gym import spaces
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class DroneRSSIEnv(gym.Env):
    def __init__(self, dataset_path):
        super(DroneRSSIEnv, self).__init__()
        # Load datasets
        # Assuming 'dataset_paths' is a list of paths to your CSV files
        self.data = pd.read_csv(dataset_path, header = 0)

        # Find the bounds for the RSSI values
        rssi_min = self.data['rssi'].min()
        rssi_max = self.data['rssi'].max()
        x_domain = [ -100,100]
        y_domain = [ -100,100]


        self.action_space = spaces.Box(low=np.array([-100, -100]), high=np.array([100, 100]), dtype=np.float32)
        # Observation space is the RSSI value
        self.observation_space = spaces.Box(low=np.array([rssi_min]), 
                                            high=np.array([rssi_max]),
                                            dtype=np.float32)
        
        # Additional initializations if needed...
        self.target_position = self.data.loc[self.data['rssi'].idxmax()]
        self.path = []  # Initialize an empty list to store the drone's path
        self.threshold_distance  = 3
        self.state = None
        
    def step(self, action):
        
        self.state = action
        rssi_value = self.interpolate_rssi(self.state)
        reward = self.calculate_reward(self.state)
        self.path.append(self.state)  # Record the new state in the path
        done = self.is_goal_reached(self.state)
        # Return the step information
        return np.array([rssi_value]), reward, done, {}

    def reset(self, initial_state=None):
        # Reset the state of the environment to an initial state , user can change the initial state
        self.state = initial_state
        self.path = [self.state]  # Reset the path to the initial state
        # Return the initial observation
        return np.array([self.interpolate_rssi(self.state)])

    def calculate_reward(self, state):
        rssi_value = self.interpolate_rssi(state)      
        return rssi_value

    def interpolate_rssi(self, state):
        # Implement interpolation to estimate RSSI at the current state
        points = self.data[['x', 'y']].values
        rssi_values = self.data['rssi'].values

        # Perform interpolation at the given state (point)
        if state[1] < 0:
            state[1] = -state[1]
        interpolated_rssi = griddata(points, rssi_values, (state[0], state[1]), method='cubic')    
        return interpolated_rssi

    def is_goal_reached(self, state):
        # Extract only the relevant x and y coordinates from target_position
        target_x = self.target_position['x']
        target_y = self.target_position['y']
        target_pos = np.array([target_x, target_y])

        # Calculate the Euclidean distance between the current state and the target position
        distance = np.linalg.norm(state - target_pos)

        # Check if the distance is less than the threshold
        return distance < self.threshold_distance
    
    def render(self, close=False, save_path=None):
        if close:
            if hasattr(self, 'fig'):
                plt.close(self.fig)
            return
        
        if not hasattr(self, 'fig') or not plt.fignum_exists(self.fig.number):
            self.setup_plot()

        if self.state is None:
            print("You need to call `reset()` before calling `render()`")
            return
        
        # Update the drone's path on the plot
        drone_x, drone_y = zip(*self.path)  # Unzip the path into x and y coordinates
        self.drone.set_data(drone_x, drone_y)  # Update the drone's trajectory on the plot
        self.drone_marker.set_data(self.state[0], self.state[1])  # Update the current drone marker position
        
        # If a save path is provided, save the current plot to a file
        if save_path:
            self.fig.savefig(save_path)
        
        # Redraw the current frame
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def setup_plot(self):
        # Set up the plot the first time render is called
        self.fig, self.ax = plt.subplots()
        self.scat = self.ax.scatter(self.data['x'], self.data['y'], c=self.data['rssi'], cmap='viridis', label='RSSI')
        plt.colorbar(self.scat, ax=self.ax, label='RSSI')
        self.drone, = self.ax.plot([], [], 'r-', linewidth=0.5, label='Drone Path')  # Line plot for the path, thinner line
        self.drone_marker, = self.ax.plot([], [], 'ro', label='Drone Position')  # Separate marker for the current position
        self.target = self.ax.plot(self.target_position[0], self.target_position[1], 'gx', label='Target Position')
        self.ax.grid(True)
        self.ax.axis('equal')
        self.ax.set_xlabel('X Coordinate')
        self.ax.set_ylabel('Y Coordinate')
        self.ax.set_title('Drone Environment')
        self.ax.legend()
        plt.ion()
        plt.show()
    
    def render3D(self, mode='human', close=False, save_path=None):
        if close:
            if hasattr(self, 'fig3D'):
                plt.close(self.fig3D)
            return
        
        if not hasattr(self, 'fig3D') or not plt.fignum_exists(self.fig3D.number):
            self.setup_plot3D()

        if self.state is None:
            print("You need to call `reset()` before calling `render3D()`")
            return

        # Unzip the path into x, y, and z coordinates
        drone_x, drone_y = zip(*self.path)
        drone_z = [self.interpolate_rssi([x, y]) for x, y in self.path]  # Interpolate the RSSI values for the path
        
        # Update the drone's path in the 3D plot
        self.drone_path3D.set_data(drone_x, drone_y)
        self.drone_path3D.set_3d_properties(drone_z)  # Update the z (RSSI) values
        
        # Update the drone marker's position in the 3D plot
        current_rssi = self.interpolate_rssi(self.state)
        self.drone_marker3D.set_data([self.state[0]], [self.state[1]])
        self.drone_marker3D.set_3d_properties([current_rssi])

        # If a save path is provided, save the current plot to a file
        if save_path:
            self.fig3D.savefig(save_path)
        
        # Redraw the current frame
        self.fig3D.canvas.draw()
        self.fig3D.canvas.flush_events()

    def setup_plot3D(self):

        self.fig3D = plt.figure()
        self.ax3D = self.fig3D.add_subplot(111, projection='3d')
        grid_x, grid_y = np.mgrid[min(self.data['x']):max(self.data['x']):100j,
                                   min(self.data['y']):max(self.data['y']):100j]

        # Interpolate the RSSI values
        points = self.data[['x', 'y']].values
        rssi_values = self.data['rssi'].values
        grid_rssi = griddata(points, rssi_values, (grid_x, grid_y), method='cubic')

        # Plotting the RSSI surface
        surf = self.ax3D.plot_surface(grid_x, grid_y, grid_rssi, cmap='viridis', linewidth=0, antialiased=False, alpha = 0.3)
        cbar = self.fig3D.colorbar(surf, shrink=0.5, aspect=5)
        cbar.set_label('RSSI')

        # Set labels and title
        self.ax3D.set_xlabel('X Coordinate')
        self.ax3D.set_ylabel('Y Coordinate')
        self.ax3D.set_zlabel('RSSI Value')
        self.ax3D.set_title('Drone Environment 3D')

        # Initialize the path and marker
        self.drone_path3D, = self.ax3D.plot([], [], [], 'r-', linewidth=1, label='Drone Path')
        self.drone_marker3D, = self.ax3D.plot([], [], [], 'ro', label='Drone Position')

        # Show the legend
        self.ax3D.legend()

        plt.ion()
        plt.show()