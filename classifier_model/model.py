import torch
import torch.nn as nn

class ProteinClassificationModel(nn.Module):
    def __init__(self, input_dim):
        super(ProteinClassificationModel, self).__init__()
        # 2-5 Hidden Layers
        # Linear
        # ReLu
        # Linear
        # ReLu
        # Linear(1 Neuron)
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, 16)
        self.fc5 = nn.Linear(16, 8)
        self.output = nn.Linear(8, 1)

    def forward(self,x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = torch.relu(self.fc4(x))
        x = torch.relu(self.fc5(x)) 
        x = self.output(x)
        return x