import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import gc

# Cleanup
gc.collect()
torch.cuda.empty_cache()

print("🔧 Starting training pipeline...")

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🖥️ Using device: {device}")

# Generate dummy data
print("📊 Generating dummy data...")
X = torch.randn(1000, 10)
y = torch.randn(1000, 1)
print(f"📐 X shape: {X.shape}, y shape: {y.shape}")

# Split into train and validation sets
print("✂️ Splitting data into train and validation sets...")
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
print(f"📐 Train shape: {X_train.shape}, Val shape: {X_val.shape}")

# Move to device
print("🚚 Moving data to device...")
X_train, y_train = X_train.to(device), y_train.to(device)
X_val, y_val = X_val.to(device), y_val.to(device)
print(f"📦 Data moved to: {device}")

# Define model
print("🧠 Defining model...")
class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(10, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.net(x)

model = SimpleNet().to(device)
print("✅ Model initialized.")
print(model)

# Loss and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)
print("⚙️ Loss function and optimizer set.")

# Training loop
print("🚀 Starting training loop...")
train_losses, val_losses = [], []
for epoch in range(100):
    model.train()
    optimizer.zero_grad()
    output = model(X_train)
    loss = criterion(output, y_train)
    loss.backward()
    optimizer.step()
    train_losses.append(loss.item())

    model.eval()
    with torch.no_grad():
        val_output = model(X_val)
        val_loss = criterion(val_output, y_val)
        val_losses.append(val_loss.item())

    if epoch % 10 == 0 or epoch == 99:
        print(f"📈 Epoch {epoch:03d} | Train Loss: {loss.item():.6f} | Val Loss: {val_loss.item():.6f}")
        print(f"🔍 Output sample: {output[:3].squeeze().tolist()}")

# Save model
torch.save(model.state_dict(), "simple_net.pt")
print("💾 Model saved as simple_net.pt")

# Plot loss curves
plt.plot(train_losses, label="Train Loss")
plt.plot(val_losses, label="Validation Loss")
plt.legend()
plt.title("Training Curve")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.savefig("loss_curve.png")
print("📉 Loss curve saved as loss_curve.png")