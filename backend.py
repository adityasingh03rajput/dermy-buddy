import torch
import torchvision.transforms as transforms
import timm
from PIL import Image
import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load custom-trained YOLOv5 model for body part detection
yolo_model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/yolov5_body_parts.pt')

# Load the pre-trained ConvNeXt model for disease classification
disease_model = timm.create_model("convnext_large", pretrained=True, num_classes=15)
disease_model.eval()

# Load the pre-trained ResNet50 model for feature extraction
feature_extractor = timm.create_model("resnet50", pretrained=True, num_classes=0)
feature_extractor.eval()

# Disease classes
disease_classes = [
    "Melanoma", "Melanocytic Nevus", "Basal Cell Carcinoma", 
    "Actinic Keratosis", "Benign Keratosis", "Dermatofibroma", "Vascular Lesion",
    "Squamous Cell Carcinoma", "Eczema", "Psoriasis", "Lentigo Maligna", "Tinea Ringworm",
    "Healthy Skin", "Cuts", "Burns"
]

# Preprocessing transforms
disease_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

feature_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def preprocess_image(image, transform):
    """Preprocesses the image for model input."""
    return transform(image).unsqueeze(0)

def extract_features(image):
    """Extracts features from the image using ResNet50."""
    img_tensor = preprocess_image(image, feature_transform)
    with torch.no_grad():
        features = feature_extractor(img_tensor)
    return features.numpy()

def predict_skin_disease(image):
    """Predicts the skin disease using ConvNeXt."""
    try:
        img_tensor = preprocess_image(image, disease_transform)
        with torch.no_grad():
            outputs = disease_model(img_tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            confidence, predicted_class = torch.max(probabilities, 0)
        return predicted_class.item(), confidence.item() * 100
    except Exception as e:
        return None, str(e)

def detect_body_part(image):
    """Detects the body part in the image using custom-trained YOLOv5."""
    try:
        # Convert PIL image to OpenCV format
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Run YOLOv5 inference
        results = yolo_model(image_cv)
        
        # Extract detected objects
        detections = results.pandas().xyxy[0]
        
        # Filter for body parts (e.g., hand, arm, face)
        body_parts = []
        for _, row in detections.iterrows():
            if row['name'] in ['hand', 'arm', 'face', 'leg']:  # Add more body parts as needed
                body_parts.append(row['name'])
        
        return body_parts[0] if body_parts else "Unknown"
    except Exception as e:
        return f"Error: {str(e)}"

def find_similar_images(image, threshold=0.9):
    """Finds similar images from the dataset based on feature similarity."""
    try:
        features = extract_features(image)
        similarities = []
        for dataset_feature in dataset_features:
            similarity = cosine_similarity(features, dataset_feature)
            similarities.append(similarity)
        max_similarity = max(similarities)
        if max_similarity >= threshold:
            index = similarities.index(max_similarity)
            return dataset_images[index], max_similarity
        else:
            return None, max_similarity
    except Exception as e:
        return None, str(e)
