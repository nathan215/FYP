import torch
import torch.nn as nn
import torch.nn.functional as F
from config import Config

config = Config()

class ResidualBlock(nn.Module):
    def __init__(self, in_features):
        super(ResidualBlock, self).__init__()
        self.linear = nn.Linear(in_features, in_features)
        self.bn = nn.BatchNorm1d(in_features)

    def forward(self, x):
        identity = x
        out = self.linear(x)
        out = self.bn(out)
        out = F.relu(out)
        out += identity  # Residual connection
        return out

class ResidualNetwork(nn.Module):
    def __init__(self, input_size, output_size):
        super(ResidualNetwork, self).__init__()
        self.input_layer = nn.Linear(input_size, config.residual_config)  # First layer
        self.residual_block1 = ResidualBlock(config.residual_config)  # First Residual Block
        self.residual_block2 = ResidualBlock(config.residual_config)  # Second Residual Block
        self.output_layer = nn.Linear(config.residual_config, output_size)  # Output layer
    
    def forward(self, x):
        x = F.relu(self.input_layer(x))
        x = self.residual_block1(x)
        x = self.residual_block2(x)  # Pass through the second residual block
        x = self.output_layer(x)
        return x

# Assuming the input size to your network is 128 (ht size), and the output size is 2 (for x,y coordinates)
input_size = 128
output_size = 2

# Instantiate the network
model = ResidualNetwork(input_size, output_size)

# Simulate a random input tensor with a batch size of 1 and input size of 128
sample_input = torch.randn(1, input_size)
# Run the sample input through the model
output = model(sample_input)

print("Output shape:", output.shape)