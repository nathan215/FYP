import sys, os
sys.path.append(os.sep+os.path.join(*sys.path[0].split(os.sep)[1: -1]))
import numpy as np
from stable_baselines3 import DDPG
from stable_baselines3.ddpg.policies import MlpPolicy
from stable_baselines3.common.noise import NormalActionNoise
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.monitor import Monitor
from env.map_esu import  DroneRSSIEnv

from stable_baselines3.common.callbacks import BaseCallback
import time

class ProgressBarCallback(BaseCallback):
    def __init__(self, total_timesteps):
        super(ProgressBarCallback, self).__init__()
        self.total_timesteps = total_timesteps
        self.start_time = time.time()

    def _on_step(self) -> bool:
        elapsed_time = time.time() - self.start_time
        progress = self.num_timesteps / self.total_timesteps
        print(f"\rProgress: {progress:.2%}, Time Elapsed: {elapsed_time:.2f}s", end='')
        return True

def train_ddpg():
    # Create the environment
    env = DroneRSSIEnv(dataset_path='path_loss_rssi_data.csv')

    # Define the action noise for exploration
    n_actions = env.action_space.shape[-1]
    action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

    # Initialize the model
    model = DDPG(MlpPolicy, env, action_noise=action_noise, verbose=1,
                 tensorboard_log="./ddpg_drone_tensorboard/")

    # Setup callbacks for checkpointing and evaluation
    checkpoint_callback = CheckpointCallback(save_freq=1000, save_path='./checkpoints/',
                                             name_prefix='ddpg_model')
    eval_env = DroneRSSIEnv(dataset_path='compiled_data.csv')  # Optional: separate environment for evaluation
    eval_env = Monitor(eval_env)
    eval_callback = EvalCallback(eval_env, best_model_save_path='./checkpoints/',
                                 log_path='./logs/', eval_freq=500,
                                 deterministic=True, render=False)

    # Train the model
    # progress_callback = ProgressBarCallback(total_timesteps=10000)
    model.learn(total_timesteps=10000, log_interval=10, callback=[checkpoint_callback, eval_callback])

    # Save the final model
    model.save("ddpg_drone_final")

if __name__ == '__main__':
    train_ddpg()
