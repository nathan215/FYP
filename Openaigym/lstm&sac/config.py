class Config:
    def __init__(self):
        self.lstm_hidden_size = 128
        self.residual_config = 128
        self.data_path = "path/to/your/data"
        self.learning_rate = 1e-3
        self.epochs = 100
        self.x_guess = [-300, 300]
        self.y_guess = [-300, 300]
        self.update_lstm_on_episode_end = True

class SACConfig:
    def __init__(self):
        self.env_name = "Pendulum-v1"
        self.policy = "Gaussian"
        self.eval = False
        self.gamma = 0.99 # discount factor for reward
        self.tau = 0.005 # target smoothing coefficient(τ)
        self.lr = 0.0003 # learning rate
        self.alpha = 0.2 # Temperature parameter α determines the relative importance of the entropy term against the reward
        self.automatic_entropy_tuning = False
        self.seed = 123456 # random seed
        self.batch_size = 128 # batch size
        self.num_steps = 100000 # maximum number of steps
        self.hidden_size = 256 # hidden size for neural networks
        self.updates_per_step = 1 # model updates per simulator step
        self.start_steps = 500 # Steps sampling random actions
        self.target_update_interval = 1 # Value target update per no. of updates per step
        self.replay_size = 100000 # size of replay buffer
        self.cuda = True # run on CUDA
        self.lstm_lr = 0.001

class map_esuConfig:
    def __init__(self):
        self.data_path = "path/to/your/data"
        self.goal_achieved_reward = 1000



