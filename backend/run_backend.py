import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from PIL import Image
import json
import os
import hashlib

app = Flask(__name__)
CORS(app)

# Încarcă modelul
model = load_model("NouErly1_mobilenetv2_plant_disease.h5")

# Încarcă clasele
with open("class_names.json", "r") as f:
    class_indices = json.load(f)
index_to_class = {v: k for k, v in class_indices.items()}
class_names = [index_to_class[i] for i in range(len(index_to_class))]

# Încarcă utilizatorii
USERS_FILE = "users.json"
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    users = load_users()
    if any(user["email"] == email for user in users):
        return jsonify({"error": "Email already registered"}), 400

    new_user = {
        "id": len(users) + 1,
        "email": email,
        "password": hash_password(password),
        "name": name
    }

    users.append(new_user)
    save_users(users)
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    users = load_users()
    for user in users:
        if user["email"] == email and user["password"] == hash_password(password):
            return jsonify({"message": "Login successful", "user": {"id": user["id"], "name": user["name"], "email": user["email"]}})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/me", methods=["GET"])
def me():
    email = request.args.get("email")
    users = load_users()
    for user in users:
        if user["email"] == email:
            return jsonify({"id": user["id"], "name": user["name"], "email": user["email"]})
    return jsonify({"error": "User not found"}), 404

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream).convert("RGB")
    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = preprocess_input(image_array)
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(image_array)
    predicted_class = class_names[np.argmax(predictions)]
    confidence = round(float(np.max(predictions)) * 100, 2)

    return jsonify({"prediction": predicted_class, "confidence": confidence})

@app.route("/plants", methods=["GET"])
def get_plants():
    plants = {
        "Tomato": [
            "Tomato_healthy",
            "Tomato_Early_blight",
            "Tomato_Late_blight",
            "Tomato_Leaf_Mold",
            "Tomato_Septoria_leaf_spot",
            "Tomato_Spider_mites_Two_spotted",
            "Tomato_Target_Spot",
            "Tomato_Tomato_YellowLeaf_Curl_Virus",
            "Tomato_Tomato_mosaic_virus"
        ],
        "Potato": [
            "Potato_healthy",
            "Potato_Early_blight",
            "Potato_Late_blight"
        ],
        "Pepper": [
            "Pepper_bell_healthy",
            "Pepper_bell_Bacterial_spot"
        ]
    }
    return jsonify(plants)


from datetime import datetime

HISTORY_FILE = "history.json"
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def load_history():
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

@app.route("/predict_with_history", methods=["POST"])
def predict_with_history():
    if 'image' not in request.files or 'email' not in request.form:
        return jsonify({"error": "Missing image or email"}), 400

    email = request.form['email']
    image_file = request.files['image']
    image = Image.open(image_file.stream).convert("RGB")
    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = preprocess_input(image_array)
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(image_array)
    predicted_class = class_names[np.argmax(predictions)]
    confidence = round(float(np.max(predictions)) * 100, 2)

    # Salvăm istoricul
    history = load_history()
    history.append({
        "email": email,
        "prediction": predicted_class,
        "confidence": confidence,
        "date": datetime.now().strftime("%Y-%m-%d")
    })
    save_history(history)

    return jsonify({"prediction": predicted_class, "confidence": confidence})

@app.route("/history", methods=["GET"])
def get_history():
    email = request.args.get("email")
    history = load_history()
    user_history = [entry for entry in history if entry["email"] == email]
    return jsonify(user_history)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
