# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

# Cria a aplicação Flask
app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem

# Rota raiz
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API Flask no ar! 🚀"}), 200

# Rota de status para testar se o app está online
@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "message": "Servidor funcionando corretamente!"}), 200

# Exemplo de rota POST (opcional)
@app.route("/echo", methods=["POST"])
def echo():
    data = request.json
    return jsonify({"received": data}), 200

# Roda o app localmente ou no Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
