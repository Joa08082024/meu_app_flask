from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import date

app = Flask(__name__)
CORS(app)  # Permite acesso externo

# --- Dados simulados (substitua por banco real se quiser) ---
usuarios = []
vales = []
relatorios = []

# --- Usuários ---
@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify(usuarios)

@app.route('/api/usuarios', methods=['POST'])
def cadastrar_usuario():
    data = request.json
    novo_usuario = {
        "id": len(usuarios)+1,
        "nome": data.get("nome"),
        "data_cadastro": data.get("data_cadastro", date.today().strftime("%Y-%m-%d"))
    }
    usuarios.append(novo_usuario)
    return jsonify({"sucesso": True, "usuario": novo_usuario})

# --- Vales ---
@app.route('/api/vales', methods=['POST'])
def lancar_vale():
    data = request.json
    vale = {
        "id": len(vales)+1,
        "usuario_id": data["usuario_id"],
        "motivo": data["motivo"],
        "numero_nota": data["numero_nota"],
        "valor": data["valor"]
    }
    vales.append(vale)
    return jsonify({"sucesso": True, "vale": vale})

# --- Relatórios ---
@app.route('/api/relatorios', methods=['GET'])
def listar_relatorios():
    resumo = {}
    for v in vales:
        key = v["motivo"]
        resumo[key] = resumo.get(key, 0) + v["valor"]
    return jsonify(resumo)

# --- Rodar app ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
