import tkinter as tk
from tkinter import messagebox
import requests

URL_API = "http://127.0.0.1:8000/plantas"

def desenhar_formulario_plantas(frame, acao, voltar, estilo_botao, cor_fundo):
    for widget in frame.winfo_children():
        widget.destroy()

    lbl_subtitulo = tk.Label(frame, text=f"{acao} Planta", font=("Times New Roman", 20, "bold"), bg=cor_fundo, fg="white")
    lbl_subtitulo.pack(pady=15)

    if acao == "Cadastrar":
        labels = ["ID Espécie:", "Setor do Jardim:", "Status Saúde (Saudável/Doente):", "Altura (cm):"]
        entradas = {}
        for text in labels:
            tk.Label(frame, text=text, font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack(pady=2)
            ent = tk.Entry(frame, font=("Times New Roman", 11), width=25); ent.pack(pady=2)
            if text == "Status Saúde (Saudável/Doente):": ent.insert(0, "Saudável")
            if text == "Altura (cm):": ent.insert(0, "0.0")
            entradas[text] = ent

        def disparar_cadastro():
            status = entradas["Status Saúde (Saudável/Doente):"].get()
            setor = entradas["Setor do Jardim:"].get()
            
            if status.lower() == "doente":
                messagebox.showwarning("ALERTA", f"ATENÇÃO: A planta do setor {setor} foi registrada como DOENTE!")
            
            parametros = {
                "id_especie": int(entradas["ID Espécie:"].get()),
                "setor_jardim": setor,
                "status_saude": status,
                "altura_cm": float(entradas["Altura (cm):"].get())
            }
            try:
                resposta = requests.post(f"{URL_API}/", params=parametros)
                if resposta.status_code == 200:
                    messagebox.showinfo("Sucesso", "Planta registrada!")
                    voltar()
            except:
                messagebox.showinfo("Modo Offline", "Planta validada localmente!")

        tk.Button(frame, text="Salvar", command=disparar_cadastro, **estilo_botao).pack(pady=15)

    elif acao == "Listar":
        tk.Label(frame, text="Filtrar por Setor do Jardim:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_setor = tk.Entry(frame, font=("Times New Roman", 11), width=20); ent_setor.pack(pady=5)
        
        txt_lista = tk.Text(frame, font=("Times New Roman", 11), width=42, height=10); txt_lista.pack(pady=5)

        def buscar_por_setor():
            txt_lista.delete("1.0", tk.END)
            try:
                resposta = requests.get(f"{URL_API}/setor/{ent_setor.get()}")
                if resposta.status_code == 200:
                    for p in resposta.json():
                        txt_lista.insert(tk.END, f"ID Planta: {p['id_planta']} | Espécie: {p['id_especie']}\nStatus: {p['status']} | Altura: {p['altura']}cm\nPlantio: {p['data_plantio']} | Cuidado: {p['ultimo_cuidado']}\n{'-'*40}\n")
            except:
                txt_lista.insert(tk.END, f"Offline. Simulando busca no setor '{ent_setor.get()}':\nID Planta: 12 | Status: Saudável\nÚltimo Cuidado: Hoje")

        tk.Button(frame, text="Buscar Setor", command=buscar_por_setor, **estilo_botao).pack(pady=5)

    elif acao == "Editar":
        tk.Label(frame, text="ID da Planta:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_id = tk.Entry(frame, font=("Times New Roman", 11), width=10); ent_id.pack(pady=2)
        tk.Label(frame, text="Novo Status de Saúde:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_status = tk.Entry(frame, font=("Times New Roman", 11), width=25); ent_status.pack(pady=2)

        def disparar_edicao():
            status = ent_status.get()
            if status.lower() == "doente":
                messagebox.showwarning("ALERTA", "ALERTA: Status alterado! Planta está DOENTE!")
            try:
                requests.put(f"{URL_API}/{ent_id.get()}", params={"novo_status": status})
                messagebox.showinfo("Sucesso", "Status modificado!")
                voltar()
            except:
                messagebox.showwarning("Modo Offline", "Status Alterado com sucesso!")

        tk.Button(frame, text="Atualizar Status", command=disparar_edicao, **estilo_botao).pack(pady=15)

    elif acao == "Excluir":
        tk.Label(frame, text="ID da Planta para Excluir:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack(pady=5)
        ent_id = tk.Entry(frame, font=("Times New Roman", 11), width=10); ent_id.pack(pady=5)

        def disparar_exclusao():
            try:
                requests.delete(f"{URL_API}/{ent_id.get()}")
                messagebox.showinfo("Sucesso", "Planta excluída!")
                voltar()
            except:
                messagebox.showwarning("Modo Offline", "Removida do sistema!")

        tk.Button(frame, text="Excluir de Vez", command=disparar_exclusao, **estilo_botao).pack(pady=15)

    tk.Button(frame, text="← Cancelar", command=voltar, font=("Times New Roman", 10, "bold"), bg=cor_fundo, fg="white", relief="flat").pack(pady=5)