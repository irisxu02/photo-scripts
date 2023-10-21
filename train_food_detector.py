import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from torchvision.models import resnet50, ResNet50_Weights


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

# load train, val, and eval data
train_data = ImageFolder("Food-5K/training", transform=transform)
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)

val_data = ImageFolder("Food-5K/validation", transform=transform)
val_loader = DataLoader(val_data, batch_size=32, shuffle=False)

eval_data = ImageFolder("Food-5K/evaluation", transform=transform)
eval_loader = DataLoader(eval_data, batch_size=32, shuffle=False)

model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, len(train_data.classes))
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 10
for epoch in range(num_epochs):
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")

# evaluate the accuracy of the model
model.eval()
total_correct = 0
total_images = 0

with torch.no_grad():
    for images, labels in eval_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total_images += labels.size(0)
        total_correct += (predicted == labels).sum().item()

accuracy = total_correct / total_images
print(f"Accuracy on evaluation data: {accuracy:.4f}")

torch.save(model.state_dict(), "food_classifier.pth")
