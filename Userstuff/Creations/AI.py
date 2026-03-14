import torch
import torch.nn as nn
import torch.optim as optim

x = torch.tensor([[1.0], [2.0], [3.0], [4.0]])
t = torch.tensor([[4.0], [5.0], [6.0], [7.0]])
model = nn.Linear(in_features=1, out_features=1)
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)
for epoch in range(1000):
    optimizer.zero_grad()
    y = model(x)
    loss = criterion(y, t)
    loss.backward()
    optimizer.step()
print("Trained weights:", model.weight.item())
print("Trained bias:", model.bias.item())
new_x = torch.tensor([[20.0]])
predicted_y = model(new_x)
print("Prediction for input 20.0:", predicted_y.item())
new_xx = torch.tensor([[15.0]])
predicted_yy = model(new_xx)
print("Prediction for input 15.0:", predicted_yy.item())


