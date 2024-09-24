MODEL_PATH = './models/RNNBest.pth'

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

torch.manual_seed(0)

class SIBIRNNModel(nn.Module):
  def __init__(self, input_size, hidden_size, num_layers, output_size):
    super(SIBIRNNModel, self).__init__()

    #Initialized RNN model parameter
    self.hidden_size = hidden_size
    self.num_layers = num_layers

    # Initialized RNN model
    self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True, nonlinearity='tanh')
    self.flatten = nn.Flatten()

    self.fc = nn.Linear(11*hidden_size, output_size)
    
    self.load_state_dict(torch.load(MODEL_PATH, weights_only=True))
    self.eval()

  def forward(self, x):

    h0 = Variable(torch.zeros(self.num_layers, x.shape[0], 20))

    out, hn = self.rnn(x, h0)
    out_flat = self.flatten(out)

    out_fc = self.fc(out_flat)
    pred = F.softmax(out_fc)

    return pred
