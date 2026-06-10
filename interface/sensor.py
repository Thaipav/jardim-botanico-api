import tkinter as tk
from tkinter import messagebox
import requests

URL_API = "http://127.0.0.1:8000/sensores"

def desenhar_formulario_sensor(frame, acao, voltar, estilo_botao, cor_fundo):
    for widget in frame.winfo_children():
        widget.destroy()

    lbl_subtitulo = tk.Label(frame, text=f"{acao} Leitura Sensor", font=("Times New Roman", 20, "bold"), bg=cor_fundo, fg="white")
    lbl_subtitulo.pack(pady=15)

    if acao == "Cadastrar":
        labels = ["Setor:", "Temperatura (°C):", "Umidade (%):"]
        entradas = {}
        for text in labels:
            tk.Label(frame, text=text, font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack(pady=2)
            ent = tk.Entry(frame, font=("Times New Roman", 11), width=25); ent.pack(pady=2)
            entradas[text] = ent

        def disparar_cadastro():
            temp = float(entradas["Temperatura (°C):"].get())
            umid = float(entradas["Umidade (%):"].get())

            if umid < 0:
                messagebox.showerror("Erro", "A umidade deve apresentar apenas valores positivos.")
                return

            if temp > 25 and umid < 30:
                diagnostico = "O ambiente está perfeito para cactos (quente e seco)."
            else:
                diagnostico = "O ambiente não está ideal para cactos no momento, coloque o sensor em um local mais apropriado, ou insira a planta adequada a esse ambiente."
            
            messagebox.showinfo("Diagnóstico do Sensor", diagnostico)

            parametros = {"setor": entradas["Setor:"].get(), "temperatura": temp, "umidade": umid}
            try:
                requests.post(f"{URL_API}/", params=parametros)
                voltar()
            except:
                voltar()

        tk.Button(frame, text="Salvar Leitura", command=disparar_cadastro, **estilo_botao).pack(pady=15)

    elif acao == "Listar":
        txt_lista = tk.Text(frame, font=("Times New Roman", 11), width=42, height=12); txt_lista.pack(pady=10)
        try:
            resposta = requests.get(f"{URL_API}/")
            if resposta.status_code == 200:
                for s in resposta.json():
                    txt_lista.insert(tk.END, f"ID: {s['id']} | Setor: {s['setor']}\nTemp: {s['temp']}°C | Umid: {s['umid']}%\nData: {s['data']}\n{'-'*40}\n")
        except:
            txt_lista.insert(tk.END, "Offline. Exemplo:\nID: 1 | Setor: Setor Norte\nTemp: 28°C | Umid: 15%\nDiagnóstico: Perfeito para Cactos")

    elif acao == "Editar":
        tk.Label(frame, text="ID da Leitura:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_id = tk.Entry(frame, font=("Times New Roman", 11), width=10); ent_id.pack(pady=2)
        tk.Label(frame, text="Novo Setor:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_setor = tk.Entry(frame, font=("Times New Roman", 11), width=25); ent_setor.pack(pady=2)
        tk.Label(frame, text="Nova Temperatura:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_temp = tk.Entry(frame, font=("Times New Roman", 11), width=25); ent_temp.pack(pady=2)
        tk.Label(frame, text="Nova Umidade:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack()
        ent_umid = tk.Entry(frame, font=("Times New Roman", 11), width=25); ent_umid.pack(pady=2)

        def disparar_edicao():
            if float(ent_umid.get()) < 0:
                messagebox.showerror("Erro", "A umidade deve apresentar apenas valores positivos.")
                return
            try:
                parametros = {"novo_setor": ent_setor.get(), "nova_temp": float(ent_temp.get()), "nova_umid": float(ent_umid.get())}
                requests.put(f"{URL_API}/{ent_id.get()}", params=parametros)
                messagebox.showinfo("Sucesso", "Leitura modificada!")
                voltar()
            except:
                messagebox.showinfo("Sucesso", "Validado localmente!")
                voltar()

        tk.Button(frame, text="Atualizar", command=disparar_edicao, **estilo_botao).pack(pady=15)

    elif acao == "Excluir":
        tk.Label(frame, text="ID do Sensor para Excluir:", font=("Times New Roman", 11), bg=cor_fundo, fg="white").pack(pady=5)
        ent_id = tk.Entry(frame, font=("Times New Roman", 11), width=10); ent_id.pack(pady=5)

        def disparar_exclusao():
            try:
                requests.delete(f"{URL_API}/{ent_id.get()}")
                messagebox.showinfo("Sucesso", "Leitura excluída!")
                voltar()
            except:
                voltar()

        tk.Button(frame, text="Excluir de Vez", command=disparar_exclusao, **estilo_botao).pack(pady=15)

    tk.Button(frame, text="← Cancelar", command=voltar, font=("Times New Roman", 10, "bold"), bg=cor_fundo, fg="white", relief="flat").pack(pady=5)