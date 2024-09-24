import torch
import numpy as np
from models.RNNModel import SIBIRNNModel
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

letter = 'a'

model = SIBIRNNModel(20, 20, 3, 26).to(device)
with open(f'./data/data/{letter}/{letter}-1.txt', 'r') as f:
    data = f.read().splitlines()

for i in range(0, len(data) - 1):
    data[i] = [float(d) for d in data[i].split(',')]
data_np = np.array([d for d in data[10:30]]).reshape((1, 11, 20))
data_torch = torch.from_numpy(data_np).float()

out = model(data_torch)
print(chr(torch.argmax(out).item() + 97))
