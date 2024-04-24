import sys, os
sys.path.append(os.sep+os.path.join(*sys.path[0].split(os.sep)[1: -1]))
from env.map_esu import DroneRSSIEnv
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.monitor import Monitor

def train_dqn(dataset_path, total_timesteps=10000):
    # Create the environment
    env = DroneRSSIEnv(dataset_path=dataset_path)
    env = Monitor(env)  # Wrap the environment with the Monitor wrapper

    # Optionally, create a vectorized environment for more efficient training
    # env = make_vec_env(lambda: env, n_envs=1)

    # Initialize the model
    model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="./dqn_drone_tensorboard/")

    # Setup callbacks for checkpointing and evaluation
    checkpoint_callback = CheckpointCallback(save_freq=1000, save_path='./checkpoints/', name_prefix='dqn_model')
    eval_env = DroneRSSIEnv(dataset_path=dataset_path)  # Optional: separate environment for evaluation
    eval_env = Monitor(eval_env)
    eval_callback = EvalCallback(eval_env, best_model_save_path='./checkpoints/', log_path='./logs/', eval_freq=500, deterministic=True, render=False)

    # Train the model
    model.learn(total_timesteps=total_timesteps, log_interval=10, callback=[checkpoint_callback, eval_callback])

    # Save the final model
    model.save("dqn_drone_final")

if __name__ == '__main__':
    dataset_path = 'path_loss_rssi_data.csv'  # Update this path
    train_dqn(dataset_path=dataset_path)