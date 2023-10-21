import sys
import os
import shutil
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image


# detect and move food images to the 'food' folder
def is_food(image_path, model, transform, device):
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
        return predicted.item() == 1  # the food class


# check if the file is an image file (no videos or raw or heic)
def is_image(filename):
    return any(
        filename.lower().endswith(extension) for extension in [".jpg", ".jpeg", ".png"]
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python find_food.py <directory_path>")
        sys.exit(1)
    root_dir = sys.argv[1]
    dest = os.path.join(root_dir, "food")

    if not os.path.exists(dest):
        os.makedirs(dest)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"using {device}")
    
    model = resnet50()
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 2)
    print("loading model...")
    model.load_state_dict(torch.load("food_classifier.pth"))
    model.to(device)
    model.eval()

    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    print("starting evaluation...")
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if is_image(file_path) and is_food(file_path, model, transform, device):
                shutil.move(file_path, os.path.join(dest, file))
                print("o")
                # if .arw file with same name exists, move that too
                arw_file = os.path.splitext(file)[0]
                arw_path = os.path.join(root, arw_file)
                if os.path.exists(arw_path):
                    shutil.move(arw_path, os.path.join(dest, arw_file))
                    print("o")
            else:
                print(".")
