import sys, os
sys.path.append(os.sep+os.path.join(*sys.path[0].split(os.sep)[1: -1]))
import gymnasium as gym
from stable_baselines3 import SAC
from stable_baselines3.sac.policies import MlpPolicy
from stable_baselines3.common.noise import NormalActionNoise
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.monitor import Monitor

from env.map_esu import DroneRSSIEnv
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.callbacks import BaseCallback

class TotalRewardCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(TotalRewardCallback, self).__init__(verbose)
        self.total_rewards = 0.0  # Initialize the total rewards

    def _on_step(self) -> bool:
        # Accumulate rewards from each step
        self.total_rewards += self.locals["rewards"].sum()  # Assuming rewards is an array
        return True

    def _on_training_end(self) -> None:
        # This method is called at the end of the training
        # Print the total accumulated rewards
        print(f"Total sum of rewards after training: {self.total_rewards}")


def train_sac(dataset_path, total_timesteps=50000, ent_coef='auto', dynamic_ent_coef=True):
    # Create the environment
    # env = DroneRSSIEnv(dataset_path=dataset_path)
    # env = Monitor(env)  # Wrap the environment with the Monitor wrapper
    
    env = gym.make("Pendulum-v1")
    # Optionally, create a vectorized environment for more efficient training
    # env = make_vec_env(lambda: env, n_envs=1)

    # Initialize the model
    model = SAC(MlpPolicy, env, ent_coef=ent_coef, verbose=1, tensorboard_log="./sac_drone_tensorboard/")

    # Setup callbacks for checkpointing and evaluation
    checkpoint_callback = CheckpointCallback(save_freq=2000, save_path='./checkpoints/', name_prefix='sac_model')

    eval_env = gym.make("Pendulum-v1")
    eval_callback = EvalCallback(eval_env, best_model_save_path='./checkpoints/', log_path='./logs/', eval_freq=500, deterministic=True, render=False)
    reward_sum_callback = TotalRewardCallback()

    model.learn(total_timesteps=total_timesteps, log_interval=10, callback=[checkpoint_callback, eval_callback,reward_sum_callback])

    # Save the final model
    model.save("sac_drone_final")


if __name__ == '__main__':
    dataset_path = 'path_loss_rssi_data.csv'  # Update this path
    train_sac(dataset_path=dataset_path, ent_coef = 'auto')
    # test agent
    # test_sac(dataset_path=dataset_path, model_path='sac_drone_final.zip')

