import tkinter as tk

def criar_menu_acoes(parent, callback_acao, voltar_menu, estilo_botao, cor_fundo):
    frame = tk.Frame(parent, bg=cor_fundo)

    lbl_titulo_acoes = tk.Label(
        frame, text="Menu", name="titulo_dinamico",
        font=("Times New Roman", 24, "bold"), bg=cor_fundo, fg="white"
    )
    lbl_titulo_acoes.pack(pady=20)

    btn_cadastrar = tk.Button(frame, text="Cadastrar", command=lambda: callback_acao("Cadastrar"), **estilo_botao)
    btn_cadastrar.pack(pady=8)

    btn_listar = tk.Button(frame, text="Listar", command=lambda: callback_acao("Listar"), **estilo_botao)
    btn_listar.pack(pady=8)

    btn_editar = tk.Button(frame, text="Editar", command=lambda: callback_acao("Editar"), **estilo_botao)
    btn_editar.pack(pady=8)

    btn_excluir = tk.Button(frame, text="Excluir", command=lambda: callback_acao("Excluir"), **estilo_botao)
    btn_excluir.pack(pady=8)

    btn_voltar_menu = tk.Button(
        frame, text="← Voltar ao Menu", command=voltar_menu,
        font=("Times New Roman", 10, "bold"), bg=cor_fundo, fg="white", relief="flat",
        activebackground=cor_fundo, activeforeground="white"
    )
    btn_voltar_menu.pack(pady=15)

    return frame