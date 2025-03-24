import torch
import torchvision.transforms as transforms
import timm
from PIL import Image

# Model configuration
MODEL_NAME = "convnext_large"
model = timm.create_model(MODEL_NAME, pretrained=True, num_classes=15)
model.eval()

disease_classes = [
    "Melanoma", "Melanocytic Nevus", "Basal Cell Carcinoma",
    "Actinic Keratosis", "Benign Keratosis", "Dermatofibroma", 
    "Vascular Lesion", "Squamous Cell Carcinoma", "Eczema", 
    "Psoriasis", "Lentigo Maligna", "Tinea Ringworm",
    "Healthy Skin", "Cuts", "Burns"
]

def preprocess_image(image):
    """Preprocess image for model input"""
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

def predict_skin_disease(image):
    """Predict skin condition from image"""
    try:
        processed_img = preprocess_image(image)
        with torch.no_grad():
            outputs = model(processed_img)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            confidence, predicted_class = torch.max(probabilities, 0)
        return predicted_class.item(), confidence.item() * 100
    except Exception as e:
        print(f"Prediction error: {e}")
        return None, 0
