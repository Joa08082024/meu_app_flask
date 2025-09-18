from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

# Lê dados
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            f.write("[]")
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Salva dados
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Rota raiz
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API Flask no ar! 🚀"}), 200

# Rota de status
@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "message": "Servidor funcionando corretamente!"}), 200

# GET para listar dados
@app.route("/dados", methods=["GET"])
def get_dados():
    data = load_data()
    return jsonify(data), 200

# POST para adicionar usuário
@app.route("/dados", methods=["POST"])
def add_dados():
    data = load_data()
    new_item = request.json

    # Garante que o ID não se repita
    ids = sorted([item["id"] for item in data])
    current = 1
    for i in ids:
        if i != current:
            break
        current += 1
    new_item["id"] = current

    data.append(new_item)
    save_data(data)
    return jsonify({"message": "Dados adicionados com sucesso!", "item": new_item}), 201

# POST para sobrescrever dados (para exclusão)
@app.route("/dados/update", methods=["POST"])
def update_dados():
    data = request.json
    save_data(data)
    return jsonify({"message": "Dados atualizados com sucesso!"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
