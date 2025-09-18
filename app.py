from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API Flask no ar! 🚀"

@app.route("/status")
def status():
    return {"status": "ok", "message": "Servidor funcionando corretamente!"}

# NÃO inclua app.run() no deploy Render
# Gunicorn irá iniciar o app automaticamente
