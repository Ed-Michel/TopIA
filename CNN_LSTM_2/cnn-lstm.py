import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torch.optim as optim
import numpy as np
from tslearn.datasets import UCR_UEA_datasets
from tslearn.preprocessing import TimeSeriesScalerMinMax
import matplotlib.pyplot as plt

dataset_name = 'ElectricDevices'

# Load and preprocess the time series data
X_train, y_train, X_test, y_test = UCR_UEA_datasets().load_dataset(dataset_name)

X_train.shape, y_train.shape, X_test.shape, y_test.shape

# Normalize the data
X_train = TimeSeriesScalerMinMax().fit_transform(X_train)
X_test = TimeSeriesScalerMinMax().fit_transform(X_test)

# Convert the data to torch tensors
X_train = torch.from_numpy(X_train).float()
X_test = torch.from_numpy(X_test).float()
y_train = torch.from_numpy(y_train).long()
y_test = torch.from_numpy(y_test).long()

# Start class from 0
y_train = y_train - 1
y_test = y_test - 1

# Create DataLoader
train_dataset = torch.utils.data.TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

test_dataset = torch.utils.data.TensorDataset(X_test, y_test)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

class CNN_LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(CNN_LSTM, self).__init__()
        self.cnn = nn.Sequential(
            nn.Conv1d(in_channels=input_size, out_channels=64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )
        self.lstm = nn.LSTM(input_size=128, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        # CNN takes input of shape (batch_size, channels, seq_len)
        x = x.permute(0, 2, 1)
        out = self.cnn(x)
        # LSTM takes input of shape (batch_size, seq_len, input_size)
        out = out.permute(0, 2, 1)
        out, _ = self.lstm(out)
        out = self.fc(out[:, -1, :])
        return out
    
input_size = X_train.shape[-1]
hidden_size = 128
num_layers = 2
num_classes = len(np.unique(y_train))

cnn_lstm = CNN_LSTM(input_size, hidden_size, num_layers, num_classes)

# Loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(cnn_lstm.parameters(), lr=0.001)

# Training loop
epochs = 200
patience = 10
best_loss = float('inf')
patience_counter = 0

for epoch in range(epochs):
    cnn_lstm.train()  # Set model to training mode
    running_loss = 0.0

    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()  # Clear gradients
        outputs = cnn_lstm(batch_X)  # Forward pass
        loss = criterion(outputs, batch_y)  # Calculate loss
        loss.backward()  # Backward pass
        optimizer.step()  # Update weights
        running_loss += loss.item()

    avg_loss = running_loss / len(train_loader)
    print(f'Epoch [{epoch + 1}/{epochs}], Loss: {avg_loss:.4f}')

    # Validation
    cnn_lstm.eval()  # Set model to evaluation mode
    val_loss = 0.0
    with torch.no_grad():
        for batch_X, batch_y in test_loader:
            outputs = cnn_lstm(batch_X)
            loss = criterion(outputs, batch_y)
            val_loss += loss.item()

    val_loss /= len(test_loader)
    print(f'Validation Loss: {val_loss:.4f}')
    
# Obtaining the Accuracy and Validation Loss from our model
cnn_lstm.eval()
val_loss = 0.0
correct = 0
total = 0

with torch.no_grad():
    for batch_X, batch_y in test_loader:
        outputs = cnn_lstm(batch_X)
        loss = criterion(outputs, batch_y)
        val_loss += loss.item()

        
        _, predicted = torch.max(outputs.data, 1)  
        total += batch_y.size(0)  
        correct += (predicted == batch_y).sum().item()  
        
val_loss /= len(test_loader)
accuracy = correct / total 
print(f'Validation Loss: {val_loss:.4f}, Accuracy: {accuracy:.4f}')

sizes = [correct, total - correct]
labels = ['Correctos', 'Incorrectos']
colors = ['#4CAF50', '#F44336']
explode = (0.1, 0)

# Creating a pie chart
plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=230)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Title
plt.title('Precisión del Modelo')
plt.show()