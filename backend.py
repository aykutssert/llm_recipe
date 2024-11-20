from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth
import openai
from secret_key import OPENAI_API_KEY
import os
import requests
from langchain_helper import get_answer, get_image_answer
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
# Flask uygulaması
app = Flask(__name__)
CORS(app)

# Firebase yapılandırması
cred = credentials.Certificate("firebaseJson.json")
firebase_admin.initialize_app(cred)

FIREBASE_API_KEY = "AIzaSyCQQ1U_zD78frg10OACqi4el7LXqrFv5DI"

# Register kullanıcı API'si
@app.route('/register', methods=['POST'])
def register_user():
    print("register_user")
    data = request.json
    email = data.get("email")
    password = data.get("password")

    try:
        user = auth.create_user(email=email, password=password)
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Login kullanıcı API'si
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Firebase REST API ile şifre doğrulama
    login_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True,
    }
    try:
        # POST isteği ile Firebase Authentication doğrulaması
        response = requests.post(login_url, json=payload)
        response_data = response.json()

        if response.status_code == 200:
            # Giriş başarılı
            return jsonify({
                "message": "Login successful",
                "email": response_data.get("email"),
                "idToken": response_data.get("idToken"),
                "refreshToken": response_data.get("refreshToken"),
            }), 200
        else:
            # Firebase hatası
            return jsonify({"error": response_data.get("error", {}).get("message", "Unknown error")}), 400

    except Exception as e:
        # Genel hata
        return jsonify({"error": str(e)}), 500

# OpenAI Prompt API
@app.route('/generate', methods=['POST'])
def generate_recipe():
    prompt = request.json.get("prompt")
    try:
        answer = get_answer(prompt)
        
        return jsonify({"response": answer}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
