import numpy as np
import pandas as pd
import math
import gymnasium as gym
from gymnasium import Env, spaces
from sklearn.linear_model import LinearRegression
from scipy.interpolate import griddata
from matplotlib import pyplot as plt

class DroneRSSIEnv(gym.Env):

    def __init__(self, dataset_path):
        super(DroneRSSIEnv, self).__init__()
        
        # Load datasets
        self.data = pd.read_csv(dataset_path, header=0)
        
        # 
        self.action_space = spaces.Box(low=np.array([-100,-100]), high=np.array([100,100]), dtype=np.float32)
        
        x_max, x_min, y_max, y_min, rssi_max, rssi_min = self._define_bounds()
        # Define observation space, 10 comibnation of x,y,rssi
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(10, 3), dtype=np.float32)


        # Additional initialization
        self.goal_delta = 5 # Distance threshold for goal achievement
        self.max_steps = 1000  # Define a maximum number of steps per episode
        self.step_counter = 0  # Initialize step counter
        self._estimate_path_loss_parameters()
        self._strogest_signal_position()
        
    def reset(self, seed=None, return_info=False, options=None):
        # Choose a random starting point
        if seed is not None:
            np.random.seed(seed)
        self.step_counter = 0  # Reset step counter
        random_x, random_y = (50,50)
        self.path = [[random_x, random_y]]
        self.location = [random_x, random_y]
        self.start_location = [random_x, random_y]
        self.state = np.zeros((10, 3), dtype=np.float32)  # Use a 2D array for the state
        self.state[0,:] = np.array([0, 0, self._get_signal_strength()])  # Set the initial state
        print(f"Resetting environment at {random_x}, {random_y} with RSSI {self._get_signal_strength()}")
        info = {}
        
        return self.state, info

    def step(self, action):
        self.step_counter += 1  # Increment step counter
        self.old_location = self.location
        self.location = [action[0]+self.start_location[0], action[1]+self.start_location[1]]
        new_rssi = self._get_signal_strength()
        new_obs = np.array([action[0],
                            action[1], new_rssi]).reshape(1, 3)
        # Shift the state by one step
        self.state[1:] = self.state[:-1]
        # add new observation
        self.state[0, :] = new_obs
        # Append the new state to the path
        self.path.append([self.location[0],self.location[1]])  # Record the new state in the path
        # Determine if the episode is done
        done = self.check_if_done()
        reward = self.calculate_reward(self.state[1,0:2],self.state[1,2], done)
        if done:
            print(f"Goal reached in {self.step_counter} steps")
            print(f"Final location: {self.location}, Final RSSI: {new_rssi}")

        if self.step_counter >= self.max_steps:
            done = True
            info = {'timeout': True}  # Optionally, add timeout information to the info dictionary
            print(f"Goal failed, Location: {self.location}, Reward: {reward}")
        else:
            info = {}     
        # Determine if the episode was truncated
        truncated = False            
        return self.state, reward, done,truncated, info
    
    def calculate_reward(self, old_location , old_rssi, is_done):
        reward = 0
        improvement = self.state[0,2]- old_rssi
        base_distance_penalty = 0.005  
        # Improvement reward
        reward += 10 * improvement
            
        # if step <5 or >30 
    
        if np.sqrt((self.location[0] - self.old_location[0])**2 + \
                        (self.location[1] - self.old_location[1])**2) > 30:
            reward -= 1

        # Goal achievement bonus
        if is_done:
            reward += 1000 # Significant bonus for reaching the goal
        return reward
    
    def check_if_done(self):
        # Check if the current state is within the goal delta
        max_signal_x, max_signal_y = self.target_position[0], self.target_position[1]
        current_x, current_y = self.location[0], self.location[1]
        distance = np.sqrt((current_x - max_signal_x) ** 2 + (current_y - max_signal_y) ** 2)
        if(distance< self.goal_delta*2):
            print(distance)
        return distance < self.goal_delta
    
    # RSSI signal strength estimation
    def _get_signal_strength(self):
        # Check if state is within bounds, use interpolation if it is
        if self._is_within_bounds():
            points = self.data[['x', 'y']].values
            rssi_values = self.data['rssi'].values
            interpolated_rssi = griddata(points, rssi_values, (self.location[0], self.location[1]), method='cubic')
            return interpolated_rssi
        else:
            # For out-of-bounds, use path-loss model to estimate RSSI
            reference_point = [0, 0]  # Same reference point used in parameter estimation
            d = np.sqrt((self.location[0] - reference_point[0])**2 + (self.location[1] - reference_point[1])**2)
            estimated_rssi = -10 * self.path_loss_n * math.log10(d) + self.path_loss_A
            return estimated_rssi

    def _is_within_bounds(self):
        x_min, x_max, y_min, y_max = -75, 75, -100, 100
        return (x_min <= self.location[0] <= x_max) and (y_min <= self.location[1] <= y_max)
    
    # Estimate path loss parameters using linear regression
    def _estimate_path_loss_parameters(self):
        # Assuming 'self.data' has 'x', 'y', and 'rssi'
        # Calculate distances for each point from a reference point (e.g., origin or another logical point)
        reference_point = [0, 0]  # Example reference point
        distances = np.sqrt((self.data['x'] - reference_point[0])**2 + (self.data['y'] - reference_point[1])**2)
        distances_log = np.log10(distances[distances > 0])  # Log of distances, excluding zero distances
        rssi_values = self.data.loc[distances > 0, 'rssi']  # Corresponding RSSI values
        
        # Perform linear regression to estimate 'n' and 'A'
        # Linear model: RSSI = -10 * n * log10(d) + A
        X = distances_log.values.reshape(-1, 1)  # Predictor
        y = rssi_values.values  # Response
        model = LinearRegression().fit(X, y)
        n = -model.coef_[0] / 10
        A = model.intercept_
        
        self.path_loss_n = n
        self.path_loss_A = A

    # it might not be strongest signal since we use grid
    def _strogest_signal_position(self):
        self.target_position = self.data.loc[self.data['rssi'].idxmax(), ['x', 'y']].values
    
    def _define_bounds(self):
        x_max = self.data['x'].max() + 2500
        x_min = self.data['x'].min() - 2500
        y_max = self.data['y'].max() + 2500
        y_min = self.data['y'].min() - 2500
        rssi_min = self.data['rssi'].min()-10
        rssi_max = self.data['rssi'].max()+10
        return x_max, x_min, y_max, y_min, rssi_max, rssi_min
    
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


if __name__ == '__main__':
    env = DroneRSSIEnv('compiled_data.csv')
    print(f"Target position: {env.target_position}")
    print(f"Path loss parameters: n={env.path_loss_n}, A={env.path_loss_A}")
    
