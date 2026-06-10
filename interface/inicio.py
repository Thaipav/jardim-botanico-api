import tkinter as tk

def criar_tela_inicio(parent, ir_para_menu, estilo_botao, cor_fundo):
    
    frame = tk.Frame(parent, bg=cor_fundo)
    
    lbl_titulo_inicial = tk.Label(
        frame, 
        text="Sistema Jardim", 
        font=("Times New Roman", 26, "bold"), 
        bg=cor_fundo, 
        fg="white"
    )
    lbl_titulo_inicial.pack(pady=30)

    btn_comecar = tk.Button(
        frame, 
        text="Começar", 
        command=ir_para_menu, 
        **estilo_botao
    )
    btn_comecar.config(height=2, width=15)
    btn_comecar.pack(pady=10)
    
    return frame