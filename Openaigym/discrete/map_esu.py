import numpy as np
import pandas as pd
import math
import gymnasium as gym
from gymnasium import Env, spaces
from sklearn.linear_model import LinearRegression
from scipy.interpolate import griddata
from matplotlib import pyplot as plt
import time
class DroneRSSIEnv(gym.Env):

    def __init__(self, dataset_path):
        super(DroneRSSIEnv, self).__init__()
        
        # # Load datasets
        # self.data = pd.read_csv(dataset_path, header=0)
        self.rssi_record = {}
        self.rssit = []
        # Define action space to be 8 actions, each representing a direction to move
        self.action_space = spaces.Discrete(8)

        # observation space is the RSSI value
        self.observation_space = spaces.Box( low = -120, high = 0, shape=(1,), dtype=np.float32)


        # Additional initialization
        self.goal_delta = 2 # Distance threshold for goal achievement
        self.max_steps = 3000  # Define a maximum number of steps per episode
        self._estimate_path_loss_parameters()
        
    def reset(self, seed=None, return_info=False, options=None):
        self.step_counter = 0  # Reset step counter
        self.total_reward = 0
        random_x, random_y = (25,25)
        self.location = [random_x, random_y]
        self.path = [[random_x, random_y]]
        self.rssi = self._get_signal_strength()
        self.state = self.discretize_state(self.rssi)  # Discretize the initial state
        return self.state  # Make sure to return the initial state


    def step(self, action):
        self.step_counter += 1  # Increment step counter
        old_rssi = self.rssi
        move = self._action_to_movement(action)
        self.location = [move[0] + self.location[0], move[1] + self.location[1]]
        new_rssi = self._get_signal_strength()
        self.state = self.discretize_state(new_rssi)  # Discretize the new state
        self.path.append(self.location)  # Record the new state in the path
        self.rssi = new_rssi  # Update the current RSSI value
        # Determine if the episode is done
        done = self.check_if_done()
        reward = self.calculate_reward(new_rssi,old_rssi, done)
        if done == True:
            info = {'goal_reached': True}
        elif self.step_counter >= self.max_steps:
            done = True
            reward -= 5
            info = {'timeout': True}
        else:
            info = {}
        self.total_reward += reward
        return self.state, reward, done, info
    
    def calculate_reward(self,new_rssi, old_rssi, is_done):
        reward = 0
        improvement = new_rssi - old_rssi
        reward = improvement
        # Goal achievement bonus
        if is_done:
            reward += 1000 # Significant bonus for reaching the goal
        if self.location[0] > 70:
            reward -= 10
            self.location[0] = 70
            self.rssi = self._get_signal_strength()
        if self.location[0] < -70:
            reward -= 10
            self.location[0] = -70
            self.rssi = self._get_signal_strength()
        if self.location[1] > 70:
            reward -= 10
            self.location[1] = 70
            self.rssi = self._get_signal_strength()
        if self.location[1] < -70:
            reward -= 10
            self.location[1] = -70
            self.rssi = self._get_signal_strength()
        return reward
    
    def _action_to_movement(self, action):
        if action == 0:
            return [0, 1]
        elif action == 1:
            return [1, 1]
        elif action == 2:
            return [1, 0]
        elif action == 3:
            return [1, -1]
        elif action == 4:
            return [0, -1]
        elif action == 5:
            return [-1, -1]
        elif action == 6:
            return [-1, 0]
        elif action == 7:
            return [-1, 1]
    
    
    def check_if_done(self):
        # Check if the current state is within the goal delta
        max_signal_x, max_signal_y = 0,0
        current_x, current_y = self.location[0], self.location[1]
        distance = np.sqrt((current_x - max_signal_x) ** 2 + (current_y - max_signal_y) ** 2)
        return distance < self.goal_delta
    
    # RSSI signal strength estimation
    def _get_signal_strength(self):
        location_tuple = tuple(self.location)  # Convert list to tuple
        if location_tuple in self.rssi_record.keys():
            return self.rssi_record[location_tuple]
        reference_points = [0,0]
        distance = np.sqrt((self.location[0] - reference_points[0])**2 + (self.location[1] - reference_points[1])**2)
        if distance == 0:
            self.rssi_record[location_tuple] = -40
            return -40
        rssi = self.path_loss_A - 10 * self.path_loss_n * np.log10(distance) + np.random.normal(0, 0.001)
        self.rssi_record[location_tuple] = rssi
        return rssi
    
    def _estimate_path_loss_parameters(self):
        self.path_loss_n = 2
        self.path_loss_A = -40

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
        self.drone_marker.set_data(self.location[0],self.location[1])  # Update the current drone marker position
        
        # If a save path is provided, save the current plot to a file
        if save_path:
            self.fig.savefig(save_path)
        
        # Redraw the current frame
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def setup_plot(self):
        # Set up the plot the first time render is called
        self.fig, self.ax = plt.subplots()
        # self.scat = self.ax.scatter(self.data['x'], self.data['y'], c=self.data['rssi'], cmap='viridis', label='RSSI')
        # plt.colorbar(self.scat, ax=self.ax, label='RSSI')
        self.drone, = self.ax.plot([], [], 'r-', linewidth=0.5, label='Drone Path')  # Line plot for the path, thinner line
        self.drone_marker, = self.ax.plot([], [], 'ro', label='Drone Position')  # Separate marker for the current position
        self.target = self.ax.plot(0,0 , 'gx', label='Target Position')
        self.ax.grid(True)
        self.ax.axis('equal')
        self.ax.set_xlabel('X Coordinate')
        self.ax.set_ylabel('Y Coordinate')
        self.ax.set_title('Drone Environment')
        self.ax.legend()
        plt.ion()
        plt.show()


if __name__ == '__main__':
    # env = DroneRSSIEnv('data/esu/compiled_data.csv')
    env = DroneRSSIEnv('generated_dataset.csv')
    print(f"Path loss parameters: n={env.path_loss_n}, A={env.path_loss_A}")
    
