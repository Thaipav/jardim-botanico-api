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
                if resposta.status_code in [200, 201]:
                    messagebox.showinfo("Sucesso", "Planta registrada!")
                    voltar()
                else:
                    messagebox.showerror("Erro na API", resposta.json().get("detail", "Erro interno no servidor."))
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao servidor da API.")

        tk.Button(frame, text="Salvar", command=disparar_cadastro, **estilo_botao).pack(pady=15)

    elif acao == "Listar":
        tk.Label(frame, text="Filtrar por Setor do Jardim:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_setor = tk.Entry(frame, font=("Times New Roman", 11), width=20); ent_setor.pack(pady=5)
        
        txt_lista = tk.Text(frame, font=("Times New Roman", 11), width=42, height=10); txt_lista.pack(pady=5)

        def buscar_por_setor():
            txt_lista.delete("1.0", tk.END)
            setor_busca = ent_setor.get().strip()
            
            if not setor_busca:
                messagebox.showwarning("Aviso", "Por favor, digite o nome de um setor.")
                return
            
            try:
                resposta = requests.get(f"{URL_API}/{setor_busca}")
                
                if resposta.status_code == 200:
                    dados = resposta.json()
                    if not dados:
                        txt_lista.insert(tk.END, f"Nenhuma planta localizada no setor '{setor_busca}'.\n")
                        return
                    
                    lista_plantas = dados if isinstance(dados, list) else [dados]
                        
                    for p in lista_plantas:
                        id_p = p.get('id_planta', p.get('id', 'N/A'))
                        esp = p.get('id_especie', 'N/A')
                        st = p.get('status_saude', p.get('status', 'N/A'))
                        alt = p.get('altura_cm', p.get('altura', 'N/A'))
                        dt = p.get('data_plantio', 'Não informada')
                        cuidad = p.get('ultimo_cuidado', 'N/A')
                        
                        txt_lista.insert(tk.END, f"ID Planta: {id_p} | Espécie: {esp}\nStatus: {st} | Altura: {alt}cm\nPlantio: {dt} | Cuidado: {cuidad}\n{'-'*40}\n")
                else:
                    txt_lista.insert(tk.END, f"Setor '{setor_busca}' não encontrado ou sem registros.")
            except requests.exceptions.ConnectionError:
                txt_lista.insert(tk.END, "Erro de conexão com o servidor local.")

        tk.Button(frame, text="Buscar Setor", command=buscar_por_setor, **estilo_botao).pack(pady=5)

    elif acao == "Editar":
        tk.Label(frame, text="ID da Planta:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_id = tk.Entry(frame, font=("Times New Roman", 11), width=10); ent_id.pack(pady=2)
        tk.Label(frame, text="Novo Status de Saúde:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_status = tk.Entry(frame, font=("Times New Roman", 11), width=25); ent_status.pack(pady=2)

        def disparar_edicao():
            id_planta = ent_id.get().strip()
            status = ent_status.get().strip()
            if not id_planta or not status:
                messagebox.showwarning("Aviso", "Informe o ID e o novo Status da planta.")
                return
                
            if status.lower() == "doente":
                messagebox.showwarning("ALERTA", "ALERTA: Status alterado! Planta está DOENTE!")
                
            try:
                resposta = requests.put(f"{URL_API}/{id_planta}/status", params={"novo_status": status})
                
                if resposta.status_code == 200:
                    messagebox.showinfo("Sucesso", "Status modificado com sucesso!")
                    voltar()
                else:
                    messagebox.showerror("Erro na API", f"Erro {resposta.status_code}: {resposta.text}")
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Erro", "Conexão perdida com a API.")

        tk.Button(frame, text="Atualizar Status", command=disparar_edicao, **estilo_botao).pack(pady=15)

    elif acao == "Excluir":
        tk.Label(frame, text="ID da Planta para Excluir:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack(pady=5)
        ent_id = tk.Entry(frame, font=("Times New Roman", 11), width=10); ent_id.pack(pady=5)

        def disparar_exclusao():
            id_planta = ent_id.get().strip()
            if not id_planta: return
            try:
                resposta = requests.delete(f"{URL_API}/{id_planta}")
                if resposta.status_code == 200:
                    messagebox.showinfo("Sucesso", "Planta excluída!")
                    voltar()
                else:
                    messagebox.showerror("Erro", "Não foi possível remover esta planta.")
            except:
                messagebox.showerror("Erro", "Falha de comunicação.")

        tk.Button(frame, text="Excluir de Vez", command=disparar_exclusao, **estilo_botao).pack(pady=15)

    tk.Button(frame, text="← Cancelar", command=voltar, font=("Times New Roman", 10, "bold"), bg=cor_fundo, fg="white", relief="flat").pack(pady=5)