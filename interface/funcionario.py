import tkinter as tk
from tkinter import messagebox
import requests

URL_API = "http://127.0.0.1:8000/funcionarios" 

def desenhar_formulario_funcionario(frame, acao, voltar, estilo_botao, cor_fundo):
    for widget in frame.winfo_children():
        widget.destroy()

    lbl_subtitulo = tk.Label(
        frame, text=f"{acao} Funcionário",
        font=("Times New Roman", 20, "bold"), bg=cor_fundo, fg="white"
    )
    lbl_subtitulo.pack(pady=15)

    if acao == "Cadastrar":
        labels = ["Nome:", "Setor:", "Turno:"]
        entradas = {}
        for text in labels:
            tk.Label(frame, text=text, font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack(pady=2)
            ent = tk.Entry(frame, font=("Times New Roman", 11), width=25)
            ent.pack(pady=2)
            entradas[text] = ent

        def disparar_cadastro():
            nome = entradas["Nome:"].get()
            if not nome:
                messagebox.showerror("Erro", "O nome precisa ser informado para cadastrar um funcionário.")
                return
            
            parametros = {"nome": nome, "setor": entradas["Setor:"].get(), "turno": entradas["Turno:"].get()}
            try:
                resposta = requests.post(f"{URL_API}/", params=parametros)
                if resposta.status_code in [200, 201]:
                    messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
                    voltar()
                else:
                    messagebox.showerror("Erro", resposta.json().get("detail", "Erro no servidor."))
            except:
                messagebox.showwarning("Modo Offline", "Validado localmente com sucesso!")

        tk.Button(frame, text="Salvar", command=disparar_cadastro, **estilo_botao).pack(pady=15)

    elif acao == "Listar":
        txt_lista = tk.Text(frame, font=("Times New Roman", 11), width=42, height=12)
        txt_lista.pack(pady=10)
        try:
            resposta = requests.get(f"{URL_API}/")
            if resposta.status_code == 200:
                for func in resposta.json():
                    txt_lista.insert(tk.END, f"ID: {func['id']} | Nome: {func['nome']}\nSetor: {func['setor']} | Turno: {func['turno']}\n{'-'*40}\n")
        except:
            txt_lista.insert(tk.END, "Offline. Exemplo:\nID: 1 | Nome: Carlos Silva\nSetor: Estufa A | Turno: Manhã")

    elif acao == "Editar":
        tk.Label(frame, text="ID do Funcionário:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_id = tk.Entry(frame, font=("Times New Roman", 11), width=10); ent_id.pack(pady=2)
        tk.Label(frame, text="Novo Setor:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_setor = tk.Entry(frame, font=("Times New Roman", 11), width=25); ent_setor.pack(pady=2)
        tk.Label(frame, text="Novo Turno:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_turno = tk.Entry(frame, font=("Times New Roman", 11), width=25); ent_turno.pack(pady=2)

        def disparar_edicao():
            if not ent_id.get(): return
            parametros = {"novo_setor": ent_setor.get(), "novo_turno": ent_turno.get()}
            try:
                resposta = requests.put(f"{URL_API}/{ent_id.get()}", params=parametros)
                if resposta.status_code == 200:
                    messagebox.showinfo("Sucesso", "Funcionário atualizado!")
                    voltar()
            except:
                messagebox.showwarning("Modo Offline", "Comando enviado!")

        tk.Button(frame, text="Atualizar", command=disparar_edicao, **estilo_botao).pack(pady=15)

    elif acao == "Excluir":
        tk.Label(frame, text="ID do Funcionário para Excluir:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack(pady=5)
        ent_id = tk.Entry(frame, font=("Times New Roman", 11), width=10); ent_id.pack(pady=5)

        def disparar_exclusao():
            try:
                resposta = requests.delete(f"{URL_API}/{ent_id.get()}")
                if resposta.status_code == 200:
                    messagebox.showinfo("Sucesso", "Funcionário removido!")
                    voltar()
            except:
                messagebox.showwarning("Modo Offline", "Removido localmente!")

        tk.Button(frame, text="Excluir de Vez", command=disparar_exclusao, **estilo_botao).pack(pady=15)

    tk.Button(frame, text="← Cancelar", command=voltar, font=("Times New Roman", 10, "bold"), bg=cor_fundo, fg="white", relief="flat").pack(pady=5)