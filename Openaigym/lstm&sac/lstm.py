import torch
import torch.nn as nn
import torch.optim as optim
from config import SACConfig 

class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTM, self).__init__()
        self.config = SACConfig()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.linear = nn.Linear(hidden_size, output_size)
        self.optimizer = optim.Adam(self.parameters(), self.config.lstm_lr )
        
    def forward(self, rssi_input):
        lstm_out, _ = self.lstm(rssi_input)
        ht = self.linear(lstm_out[:, -1, :])  # Take the output of the last LSTM cell
        return ht

    def custom_loss(predictions, rewards, alpha=2.0):
        """
        Custom loss function that penalizes errors in predicting negative rewards more.
        predictions: The LSTM output interpreted as reward predictions.
        rewards: Actual rewards received.
        alpha: Factor to weigh negative rewards (alpha > 1 means more penalty).
        """
        loss = 0.0
        for pred, reward in zip(predictions, rewards):
            if reward < 0:
                loss += alpha * (pred - reward) ** 2  # Higher penalty for negative rewards
            else:
                loss += (pred - reward) ** 2
        loss /= len(predictions)  # Mean loss
        return loss

    def compute_loss(self, predictions, rewards):
        """
        Computes a loss based on the model's predictions and received rewards.
        This function needs to be tailored based on how predictions relate to rewards.
        """
        # Example: Mean Squared Error (MSE) if predictions and rewards are directly comparable.
        return nn.MSELoss()(predictions, rewards)

    def update(self, rewards):
        """
        Updates the model using the rewards received at the end of an episode.
        This method might need to adapt rewards into a suitable format for training.
        """
        # Process rewards: This step is highly specific to your problem setup.
        # For demonstration, assuming rewards can be directly used for updating.
        processed_rewards = torch.tensor(rewards, dtype=torch.float32)

        # Assuming the model outputs predictions corresponding to these rewards in its last forward pass:
        predictions = self.last_ht  # You'll need to store this from the last forward pass.

        # Compute loss
        loss = self.compute_loss(predictions, processed_rewards)

        # Backpropagation
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    # Additional utility functions as needed, e.g., for preprocessing RSSI signals.
