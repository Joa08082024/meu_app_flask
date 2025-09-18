# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem

DATA_FILE = "data.json"

# Função para ler dados
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Função para salvar dados
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

# Rota GET para listar dados
@app.route("/dados", methods=["GET"])
def get_dados():
    data = load_data()
    return jsonify(data), 200

# Rota POST para adicionar dados
@app.route("/dados", methods=["POST"])
def add_dados():
    data = load_data()
    new_item = request.json
    data.append(new_item)
    save_data(data)
    return jsonify({"message": "Dados adicionados com sucesso!", "item": new_item}), 201

# Rota DELETE para excluir usuário
@app.route("/dados/<int:user_id>", methods=["DELETE"])
def delete_usuario(user_id):
    data = load_data()
    data = [u for u in data if u["id"] != user_id]
    save_data(data)
    return jsonify({"message": f"Usuário {user_id} excluído com sucesso!"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
