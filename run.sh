#!/bin/bash

# Install system dependencies (for libGL.so.1)
sudo apt-get update
sudo apt-get install -y libgl1-mesa-glx

# Install Python dependencies
pip install -r requirements.txt

# Download YOLOv5 and custom-trained model
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
cd ..

# Run the Streamlit app
streamlit run app.py
