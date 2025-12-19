from flask import Flask, request, jsonify
import cv2
import numpy as np
import mediapipe as mp
import hashlib
import requests

app = Flask(__name__)

# CONFIGURATION
QDRANT_URL = "https://TON-URL-QDRANT-CLOUD" # (On verra ça après)
API_BANK_URL = "https://handpay-api-xxxx.onrender.com" # Mets ton lien Render ici !

# INIT MEDIAPIPE
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)

def get_palm_vector(hand_landmarks):
    points = []
    for lm in hand_landmarks.landmark:
        points.append(lm.x); points.append(lm.y); points.append(lm.z)
    vector = points[:128]
    while len(vector) < 128: vector.append(0.0)
    return vector

@app.route('/', methods=['GET'])
def home():
    return "HandPay AI Brain is Online 🧠"

@app.route('/scan', methods=['POST'])
def scan_hand():
    # 1. Recevoir l'image du téléphone
    if 'image' not in request.files:
        return jsonify({"error": "Aucune image envoyée"}), 400
    
    file = request.files['image']
    # Convertir en format lisible par OpenCV
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # 2. Analyser la main
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if not results.multi_hand_landmarks:
        return jsonify({"error": "Aucune main détectée"}), 400

    # 3. Extraire le vecteur
    vector = get_palm_vector(results.multi_hand_landmarks[0])
    
    # 4. (Ici on ferait la recherche Qdrant comme avant)
    # Pour le test rapide, on renvoie juste le token
    vector_str = str(vector).encode('utf-8')
    token = hashlib.sha256(vector_str).hexdigest()

    return jsonify({
        "message": "Main analysée avec succès",
        "hand_token": token
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)