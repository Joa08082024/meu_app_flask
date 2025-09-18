from flask import Flask, jsonify, request
from flask_cors import CORS
import os

# Cria a aplicação Flask
app = Flask(__name__)
CORS(app)

# Rota raiz
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API Flask no ar! 🚀"}), 200

# Rota de status
@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "message": "Servidor funcionando corretamente!"}), 200

# Rota POST de teste
@app.route("/echo", methods=["POST"])
def echo():
    data = request.json
    return jsonify({"received": data}), 200

# Executa o app localmente ou no Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
