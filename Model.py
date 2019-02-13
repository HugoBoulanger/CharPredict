import torch
import torch.nn as nn
import torch.nn.functional as F

class HighwayLayer(nn.Module):
    def __init__():
        # TODO : Les arguments
        self.l = nn.Linear()
        self.relu = nn.ReLU()
        
    def forward(self, inputs):
        # TODO
        
class Model(nn.Module):
    def __init__():
        # TODO : les arguments
        self.embed = nn.Embedding()
        self.conv = nn.Conv1d()
        self.mp = nn.MaxPool1d()
        self.hw = HighwayLayer()
        self.lstm = nn.LSTM()
        self.out = nn.Linear()
        
        self.do = nn.Dropout()
        
    def forward(self, inputs):
        # TODO