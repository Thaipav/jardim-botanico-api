import tkinter as tk

def criar_menu_opcoes(parent, ir_para_acoes, voltar_inicio, estilo_botao, cor_fundo):
    frame = tk.Frame(parent, bg=cor_fundo)

    lbl_titulo_opcoes = tk.Label(
        frame, 
        text="O que deseja?", 
        font=("Times New Roman", 24, "bold"), 
        bg=cor_fundo, 
        fg="white"
    )
    lbl_titulo_opcoes.pack(pady=20)

    btn_especie = tk.Button(frame, text="Espécie", command=lambda: ir_para_acoes("Espécie"), **estilo_botao)
    btn_especie.pack(pady=8)

    btn_funcionario = tk.Button(frame, text="Funcionário", command=lambda: ir_para_acoes("Funcionário"), **estilo_botao)
    btn_funcionario.pack(pady=8)

    btn_plantas = tk.Button(frame, text="Plantas", command=lambda: ir_para_acoes("Plantas"), **estilo_botao)
    btn_plantas.pack(pady=8)

    btn_sensor = tk.Button(frame, text="Sensor", command=lambda: ir_para_acoes("Sensor"), **estilo_botao)
    btn_sensor.pack(pady=8)

    btn_voltar_inicio = tk.Button(
        frame, text="← Voltar", command=voltar_inicio,
        font=("Times New Roman", 10, "bold"), bg=cor_fundo, fg="white", relief="flat",
        activebackground=cor_fundo, activeforeground="white"
    )
    btn_voltar_inicio.pack(pady=15)

    return frame