import tkinter as tk
from tkinter import messagebox
import requests

URL_API = "http://127.0.0.1:8000/especies"

def desenhar_formulario_especie(frame, acao, voltar, estilo_botao, cor_fundo):
    for widget in frame.winfo_children():
        widget.destroy()

    lbl_subtitulo = tk.Label(
        frame, text=f"{acao} Espécie",
        font=("Times New Roman", 20, "bold"), bg=cor_fundo, fg="white"
    )
    lbl_subtitulo.pack(pady=15)

    if acao == "Cadastrar":
        labels = ["Nome:", "Frequência de Rega (dias):", "Luminosidade:", "Categoria:", "Origem:"]
        entradas = {}
        
        for label_text in labels:
            lbl = tk.Label(frame, text=label_text, font=("Times New Roman", 11), bg=cor_fundo, fg="white")
            lbl.pack(pady=2)
            ent = tk.Entry(frame, font=("Times New Roman", 11), width=25)
            ent.pack(pady=2)
            entradas[label_text] = ent
            
        def disparar_cadastro():
            nome = entradas["Nome:"].get()
            rega = entradas["Frequência de Rega (dias):"].get()
            
            if not nome:
                messagebox.showerror("Erro", "O nome da espécie é obrigatório.")
                return
            try:
                rega_int = int(rega)
            except ValueError:
                messagebox.showerror("Erro", "A rega deve ser um número inteiro.")
                return
                
            if rega_int < 0:
                messagebox.showerror("Erro", "A rega não pode ser negativa!")
                return
            if "cacto" in nome.lower() and rega_int > 1:
                messagebox.showerror("Erro", "Cactos devem ser regados no máximo uma vez por semana.")
                return
            
            parametros = {
                "nome": nome, 
                "frequencia_rega": rega_int,
                "luminosidade": entradas["Luminosidade:"].get(),
                "categoria": entradas["Categoria:"].get(),
                "origem": entradas["Origem:"].get()
            }
            
            try:
                resposta = requests.post(f"{URL_API}/", params=parametros)
                if resposta.status_code in [200, 201]:
                    messagebox.showinfo("Sucesso", "Espécie cadastrada com sucesso!")
                    voltar()
                else:
                    messagebox.showerror("Erro da API", resposta.json().get("detail", "Erro ao cadastrar."))
            except requests.exceptions.ConnectionError:
                messagebox.showwarning("Modo Offline", "Regras validadas! Ligue o Uvicorn para salvar na API.")

        btn_salvar = tk.Button(frame, text="Salvar", command=disparar_cadastro, **estilo_botao)
        btn_salvar.pack(pady=15)

    elif acao == "Listar":
        txt_lista = tk.Text(frame, font=("Times New Roman", 11), width=42, height=12)
        txt_lista.pack(pady=10)
        
        try:
            resposta = requests.get(f"{URL_API}/")
            if resposta.status_code == 200:
                especies = resposta.json()
                if not especies:
                    txt_lista.insert(tk.END, "Nenhuma espécie cadastrada ainda.")
                for esp in especies:
                    txt_lista.insert(tk.END, f"ID: {esp['id']} | Nome: {esp['nome']}\nRega: {esp['rega']} | Solo: {esp['solo']}\n{'-'*40}\n")
            else:
                txt_lista.insert(tk.END, "Erro ao buscar a lista na API.")
        except requests.exceptions.ConnectionError:
            txt_lista.insert(tk.END, "Uvicorn desligado.\nExemplo simulado:\nID: 1 | Nome: Cacto Bola\nRega: 1 | Solo: solo humífero")

    elif acao == "Editar":
        tk.Label(frame, text="ID da Espécie que deseja Editar:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_id = tk.Entry(frame, font=("Times New Roman", 11), width=10)
        ent_id.pack(pady=2)
        
        tk.Label(frame, text="Novo Nome:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_nome = tk.Entry(frame, font=("Times New Roman", 11), width=25)
        ent_nome.pack(pady=2)
        
        tk.Label(frame, text="Nova Frequência de Rega (freq):", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_rega = tk.Entry(frame, font=("Times New Roman", 11), width=25)
        ent_rega.pack(pady=2)
        
        def disparar_edicao():
            id_alvo = ent_id.get()
            nome = ent_nome.get()
            rega = ent_rega.get()
            
            if not id_alvo or not nome or not rega:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios para editar.")
                return
                
            if "cacto" in nome.lower() and int(rega) > 1:
                messagebox.showerror("Erro", "Cactos devem ser regados no máximo uma vez por semana.")
                return
            
            parametros = {"nome": nome, "freq": int(rega)}
            
            try:
                resposta = requests.put(f"{URL_API}/{id_alvo}", params=parametros)
                if resposta.status_code == 200:
                    messagebox.showinfo("Sucesso", "Espécie editada com sucesso!")
                    voltar()
                else:
                    messagebox.showerror("Erro", resposta.json().get("detail", "Espécie não encontrada."))
            except requests.exceptions.ConnectionError:
                messagebox.showwarning("Modo Offline", "Regras validadas! Ligue o Uvicorn para aplicar as alterações.")

        btn_editar = tk.Button(frame, text="Atualizar", command=disparar_edicao, **estilo_botao)
        btn_editar.pack(pady=15)

    elif acao == "Excluir":
        tk.Label(frame, text="ID da Espécie para Excluir:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack(pady=5)
        ent_id = tk.Entry(frame, font=("Times New Roman", 11), width=10)
        ent_id.pack(pady=5)
        
        def disparar_exclusao():
            id_alvo = ent_id.get()
            if not id_alvo:
                messagebox.showerror("Erro", "Digite um ID válido.")
                return
                
            try:
                resposta = requests.delete(f"{URL_API}/{id_alvo}")
                if resposta.status_code == 200:
                    messagebox.showinfo("Sucesso", "Espécie excluída do sistema!")
                    voltar()
                else:
                    messagebox.showerror("Erro", "Não é possível excluir esta espécie, pois existem plantas vinculadas a ela.")
            except requests.exceptions.ConnectionError:
                messagebox.showwarning("Modo Offline", "Ligue o Uvicorn para efetivar a exclusão no banco de dados.")

        btn_deletar = tk.Button(frame, text="Excluir de Vez", command=disparar_exclusao, **estilo_botao)
        btn_deletar.pack(pady=15)

    btn_cancelar = tk.Button(
        frame, text="← Cancelar", command=voltar,
        font=("Times New Roman", 10, "bold"), bg=cor_fundo, fg="white", relief="flat",
        activebackground=cor_fundo, activeforeground="white"
    )
    btn_cancelar.pack(pady=5)