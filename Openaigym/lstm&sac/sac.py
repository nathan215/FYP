import gym
import numpy as np
import torch
from torch.utils.tensorboard import SummaryWriter
import itertools
import datetime
from sac_class import SAC  
from sac_replay_memory import ReplayMemory  
from config import SACConfig ,map_esuConfig
from lstm import LSTM

class SACModel:
    def __init__(self, config):
        self.config = config
        self.map_esu_config = map_esuConfig()
        self.env = gym.make(config.env_name)
        self.agent = SAC(self.env.observation_space.shape[0], self.env.action_space, config)
        self.memory = ReplayMemory(config.replay_size, config.seed)
        self.writer = SummaryWriter(f'runs/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_{config.env_name}_{config.policy}{"_autotune" if config.automatic_entropy_tuning else ""}')
        self.lstm_model = LSTM(input_size=config.lstm_input_size, hidden_size=config.lstm_hidden_size, output_size=config.lstm_output_size)
        torch.manual_seed(config.seed)
        np.random.seed(config.seed)

    def train(self):
        total_numsteps = 0
        updates = 0
        for i_episode in itertools.count(1):
            
            rewards = []
            episode_reward = 0
            episode_steps = 0
            done = False
            state = self.env.reset()
            state = state[0] if isinstance(state, tuple) else state

            if config.update_lstm_on_episode_end:
                rssi_input = [state]
                state = self.lstm_model.forward(rssi_input)

            while not done:

                if config.start_steps > total_numsteps:
                    action = self.env.action_space.sample()  # Sample random action
                else:
                    action = self.agent.select_action(state)  # Sample action from policy
                
                if len(self.memory) > config.batch_size:
                    # Number of updates per step in environment
                    for i in range(config.updates_per_step):
                        # Update parameters of all the networks
                        critic_1_loss, critic_2_loss, policy_loss, ent_loss, alpha = self.agent.update_parameters(self.memory, config.batch_size, updates)

                        self.writer.add_scalar('loss/critic_1', critic_1_loss, updates)
                        self.writer.add_scalar('loss/critic_2', critic_2_loss, updates)
                        self.writer.add_scalar('loss/policy', policy_loss, updates)
                        self.writer.add_scalar('loss/entropy_loss', ent_loss, updates)
                        self.writer.add_scalar('entropy_temprature/alpha', alpha, updates)
                        updates += 1

                new_state, reward, done, _ , _= self.env.step(action) # Step

                if config.update_lstm_on_episode_end:
                    rewards.append(reward)
                    rssi_input.append(next_state)
                    next_state = self.lstm_model.forward(rssi_input)

                episode_steps += 1
                total_numsteps += 1
                episode_reward += reward
                
                # add nex_rssi to lstm and get the new state

                mask = 1 if episode_steps == self.env._max_episode_steps else float(not done)

                self.memory.push(state, action, reward, next_state, mask) # Append transition to memory

                state = next_state

                if episode_steps >= self.env._max_episode_steps:
                    done = True
                    

            # update the lstm model
            if config.update_lstm_on_episode_end:
                if done:
                    rewards[-1] -= self.map_esu_config.goal_achieved_reward
                    for i in range(len(rewards)-1):
                        rewards[i] += self.map_esu_config.goal_achieved_reward
                self.lstm_model.update(rssi_input,rewards)
            
            if total_numsteps > config.num_steps:
                break
            
            self.writer.add_scalar('reward/train', episode_reward, i_episode)
            print("Episode: {}, total numsteps: {}, episode steps: {}, reward: {}".format(i_episode, total_numsteps, episode_steps, round(episode_reward, 2)))

            if i_episode % 10 == 0 and config.eval is True:
                avg_reward = 0.
                episodes = 10
                for _  in range(episodes):
                    state = self.env.reset()
                    state = state[0] if isinstance(state, tuple) else state
                    episode_reward = 0
                    done = False
                    episode_steps = 0
                    Fail = False
                    if config.update_lstm_on_episode_end:
                        rssi_input = [state]
                        state = self.lstm_model.forward(rssi_input)
                        
                    while not done:
                        action = self.agent.select_action(state, evaluate=True)

                        next_rssi, reward, done, _,_ = self.env.step(action)

                        if config.update_lstm_on_episode_end:
                            rssi_input.append(next_rssi)
                            next_state = self.lstm_model.forward(rssi_input)

                        episode_reward += reward
                        state = next_state
                        episode_steps += 1

                        if episode_steps >= self.env._max_episode_steps:
                            Fail = True
                            done = True
                    avg_reward += episode_reward
                avg_reward /= episodes


                self.writer.add_scalar('avg_reward/test', avg_reward, i_episode)

                print("----------------------------------------")
                print("Test Episodes: {}, Avg. Reward: {}".format(episodes, round(avg_reward, 2)), "Fail: ", Fail)
                print("----------------------------------------")

        self.env.close()

    def select_action(self, state, evaluate=False):
        return self.agent.select_action(state, evaluate)


if __name__ == '__main__':
    config = SACConfig()
    sac_model = SACModel(config)
    sac_model.train()