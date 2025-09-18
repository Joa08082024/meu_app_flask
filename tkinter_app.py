import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

# URL base da API Flask
API_URL = "http://127.0.0.1:5000"  # ou substitua pela URL do Render

# ---------------- Funções ---------------- #
def atualizar_treeview():
    try:
        resp = requests.get(f"{API_URL}/dados")
        resp.raise_for_status()
        data = resp.json()
        for i in tree.get_children():
            tree.delete(i)
        for item in data:
            tree.insert("", tk.END, values=(item.get("id"), item.get("nome"), item.get("data")))
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar dados: {e}")

def proximo_id(data):
    ids = sorted([item["id"] for item in data])
    current = 1
    for i in ids:
        if i != current:
            return current
        current += 1
    return current

def cadastrar_usuario():
    nome = entry_nome.get().strip()
    data_cadastro = entry_data.get().strip()

    if not nome or not data_cadastro:
        messagebox.showwarning("Erro", "Preencha todos os campos!")
        return

    try:
        datetime.strptime(data_cadastro, "%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("Erro", "Data deve estar no formato YYYY-MM-DD")
        return

    # Obtem dados atuais para gerar ID
    resp = requests.get(f"{API_URL}/dados")
    resp.raise_for_status()
    data = resp.json()
    next_id = proximo_id(data)

    novo_usuario = {
        "id": next_id,
        "nome": nome,
        "data": data_cadastro
    }

    resp = requests.post(f"{API_URL}/dados", json=novo_usuario)
    if resp.status_code == 201:
        atualizar_treeview()
        entry_nome.delete(0, tk.END)
        entry_data.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "Falha ao cadastrar usuário!")

def excluir_usuario():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Erro", "Selecione um usuário para excluir")
        return
    for item in selected:
        id_user = tree.item(item, "values")[0]
        try:
            # Exclui localmente do JSON
            resp = requests.get(f"{API_URL}/dados")
            resp.raise_for_status()
            data = resp.json()
            data = [u for u in data if u["id"] != int(id_user)]
            requests.post(f"{API_URL}/dados", json=data)  # reescreve todo JSON
            atualizar_treeview()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao excluir usuário: {e}")

# ---------------- Interface Tkinter ---------------- #
root = tk.Tk()
root.title("Cadastro de Usuários")
root.geometry("500x400")

frame_cadastro = tk.Frame(root)
frame_cadastro.pack(pady=10)

tk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(frame_cadastro)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_cadastro, text="Data (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
entry_data = tk.Entry(frame_cadastro)
entry_data.grid(row=1, column=1, padx=5, pady=5)

btn_cadastrar = tk.Button(frame_cadastro, text="Cadastrar", command=cadastrar_usuario)
btn_cadastrar.grid(row=2, column=0, columnspan=2, pady=10)

btn_excluir = tk.Button(root, text="Excluir Selecionado", command=excluir_usuario)
btn_excluir.pack(pady=5)

tree = ttk.Treeview(root, columns=("ID", "Nome", "Data"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Data", text="Data de Cadastro")
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

atualizar_treeview()

root.mainloop()
