import torch
from lstm import LSTMModel
from sac import SACModel
from residual_network import ResidualNetwork
from data_loader import DataLoader
from config import Config
from utils import calculate_loss2, update_position
import random

class CompositeModel(torch.nn.Module):
    def __init__(self, lstm_model, sac_model, residual_network):
        super(CompositeModel, self).__init__()
        self.lstm_model = lstm_model
        self.sac_model = sac_model
        self.residual_network = residual_network

    def forward(self, signal, current_x, current_y, current_angle):
        ht = self.lstm_model(signal)
        action, revenue, done = self.sac_model.select_action(ht, evaluate=False)  # Adjust based on SACModel's interface
        predicted_x_y = self.residual_network(ht)

        new_x, new_y, new_angle = update_position(action, current_x, current_y, current_angle)
        
        return predicted_x_y, revenue, done, new_x, new_y, new_angle


def train():
    config = Config()
    data_loader = DataLoader(config.data_path)
    lstm_model = LSTMModel(config.lstm_hidden_size)
    sac_model = SACModel(config.sac_config)
    residual_network = ResidualNetwork(config.residual_config)

    composite_model = CompositeModel(lstm_model, sac_model, residual_network)
    optimizer = torch.optim.Adam(composite_model.parameters(), lr=config.learning_rate)

    real_x_y = torch.tensor([0, 0])

    for epoch in range(config.epochs):
        start_x, start_y = random.choice(config.x_guess), random.choice(config.y_guess)
        current_x, current_y = start_x, start_y
        current_angle = 0
        done = False  # Initialize done

        while not done:
            signal = data_loader.get_signal(current_x, current_y)
            predicted_x_y, revenue, done, current_x, current_y, current_angle = composite_model(signal, current_x, current_y, current_angle)

            loss1 = -revenue  # Assuming revenue is positive for beneficial actions
            loss2 = calculate_loss2(predicted_x_y, real_x_y)
            loss = loss1 + loss2

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            

if __name__ == "__main__":
    train()
