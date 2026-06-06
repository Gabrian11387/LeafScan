# LeafScan - AI Plant Disease Detection System

LeafScan is an AI-powered web application that identifies plant diseases from leaf images using a deep learning model based on MobileNetV2. The system combines a Flask REST API backend, a React frontend, and a trained image classification model to provide accurate disease predictions and treatment recommendations.

## Key Achievements

- Trained MobileNetV2 on 54,000+ images from the PlantVillage dataset
- Achieved 97.3% validation accuracy
- Developed a full-stack architecture using Flask and React
- Implemented REST APIs and an end-to-end image processing pipeline

## Features

- Plant disease detection from uploaded leaf images
- Deep learning classification using MobileNetV2
- Prediction confidence score
- Disease information and treatment recommendations
- User authentication and authorization
- Responsive web interface

## Tech Stack

### Frontend
- React
- JavaScript
- Axios
- CSS

### Backend
- Python
- Flask
- REST APIs

### AI & Data Processing
- TensorFlow
- Keras
- MobileNetV2
- OpenCV
- NumPy
- Pillow

## Machine Learning

The model was trained using transfer learning with MobileNetV2 on the PlantVillage dataset, which contains over 54,000 images of healthy and diseased plant leaves across multiple crop species.

The training pipeline included:
- Image preprocessing and normalization
- Dataset splitting into training, validation, and test sets
- Transfer learning and fine-tuning
- Performance evaluation and model optimization

## System Architecture

```text
React Frontend
      │
      ▼
 Flask REST API
      │
      ▼
 MobileNetV2 Model
      │
      ▼
 Disease Prediction & Analysis
```

## Workflow

1. User uploads a leaf image.
2. The image is sent to the Flask API.
3. The model analyzes the image.
4. The predicted disease is returned.
5. The application displays:
   - Disease name
   - Confidence score
   - Disease information
   - Treatment recommendations

## Installation

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## Academic Project

LeafScan was developed as a Bachelor's Degree project in Computer Science and demonstrates the integration of Artificial Intelligence, Computer Vision, Deep Learning, and Full-Stack Web Development into a practical plant disease diagnosis system.

## Author

**Costan Gabriel-Cristian**

Software Engineer

LinkedIn:
https://www.linkedin.com/in/gabriel-costan-b9a92a269