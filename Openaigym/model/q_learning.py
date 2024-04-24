import sys, os
sys.path.append(os.sep+os.path.join(*sys.path[0].split(os.sep)[1: -1]))
import numpy as np
from gym import spaces
from tqdm import tqdm
from discrete.map_esu import DroneRSSIEnv
import pickle
import matplotlib.pyplot as plt

def plot_trajectory(env):
    """
    Plots the trajectory of the drone in the environment.
    Assumes env.path contains the (x, y) positions visited by the drone.
    """
    # Extract x and y coordinates from the path
    x_coords, y_coords = zip(*env.path)
    
    # Plot the trajectory
    plt.figure(figsize=(10, 6))
    plt.plot(x_coords, y_coords, marker='o', linestyle='-', markersize=5, linewidth=2, label='Trajectory')
    
    # Optionally, plot the start and end points
    plt.scatter([x_coords[0]], [y_coords[0]], color='green', zorder=5, s=100, label='Start')
    plt.scatter([x_coords[-1]], [y_coords[-1]], color='red', zorder=5, s=100, label='End')
    
    plt.title('Drone Trajectory to Strongest Signal')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.grid(True)
    plt.show()

class QLearningAgent:
    def __init__(self, action_space, state_space_size, learning_rate=0.1, discount_factor=0.95, epsilon=1.0, epsilon_decay=0.99, min_epsilon=0.01):
        self.action_space = action_space
        self.state_space_size = state_space_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        # Initialize Q-table, assuming state_space_size is an integer representing the number of discretized states
        self.q_table = np.zeros((state_space_size, action_space.n))

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return self.action_space.sample()  # Explore
        else:
            return np.argmax(self.q_table[state])  # Exploit

    def update_q_table(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state, best_next_action]
        td_error = td_target - self.q_table[state, action]
        self.q_table[state, action] += self.learning_rate * td_error

    def update_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

def test_agent(env, agent, episodes=10):
    total_rewards = []
    successful_episodes = 0

    for episode in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0
        while not done:
            action = agent.choose_action(state) 
            next_state, reward, done, info = env.step(action)
            total_reward += reward
            state = next_state
            if info.get('timeout', False):
                break
        total_rewards.append(total_reward)
        print(info)
        if info.get('goal_reached', False):
            successful_episodes += 1

        print(f"Episode {episode + 1}: Total Reward = {total_reward}")
        plot_trajectory(env)

    avg_reward = sum(total_rewards) / episodes
    success_rate = successful_episodes / episodes
    print(f"Average Reward: {avg_reward}")
    print(f"Success Rate: {success_rate * 100}%")

# Integrate with DroneRSSIEnv
if __name__ == '__main__':
    env = DroneRSSIEnv('generated_dataset.csv')
    agent = QLearningAgent(env.action_space, state_space_size=100000)  # Assuming 100 discretized states for demonstration

    episodes = 3000
    for episode in tqdm(range(episodes)):
        state = env.reset()
        done = False

        while not done:
            action = agent.choose_action(state)
            next_state, reward, done, info = env.step(action)
            agent.update_q_table(state, action, reward, next_state)
            state = next_state
        if not info.get('timeout', False):
            print(f"Episode {episode + 1} successfully completed")
        # Assuming your QLearningAgent instance is named `agent`
    with open('q_table.pkl', 'wb') as f:
        pickle.dump(agent.q_table, f)

    print("Q-table saved to q_table.pkl")
    test_agent(env, agent, episodes=100)


