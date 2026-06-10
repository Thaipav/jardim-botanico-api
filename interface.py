import tkinter as tk

from interface.inicio import criar_tela_inicio
from interface.menu_opcoes import criar_menu_opcoes
from interface.menu_acoes import criar_menu_acoes
from interface.especie import desenhar_formulario_especie
from interface.funcionario import desenhar_formulario_funcionario
from interface.planta import desenhar_formulario_plantas
from interface.sensor import desenhar_formulario_sensor

janela = tk.Tk()
janela.title("Sistema Jardim Inteligente")
janela.geometry("450x550") 

MARROM_PASTEL_ESCURO = "#4A3B32"  
janela.configure(bg=MARROM_PASTEL_ESCURO)

estilo_botao_menu = {
    "font": ("Times New Roman", 12, "bold"),
    "bg": "white",
    "fg": MARROM_PASTEL_ESCURO, 
    "width": 18,
    "height": 1,
    "relief": "flat",
    "activebackground": "white",
    "activeforeground": MARROM_PASTEL_ESCURO
}

categoria_atual = ""

frame_inicial = tk.Frame(janela, bg=MARROM_PASTEL_ESCURO)
frame_opcoes = tk.Frame(janela, bg=MARROM_PASTEL_ESCURO)
frame_acoes = tk.Frame(janela, bg=MARROM_PASTEL_ESCURO)
frame_formulario = tk.Frame(janela, bg=MARROM_PASTEL_ESCURO)

def esconder_todas_telas():
    frame_inicial.pack_forget()
    frame_opcoes.pack_forget()
    frame_acoes.pack_forget()
    frame_formulario.pack_forget()

def abrir_menu_opcoes():
    esconder_todas_telas()
    frame_opcoes.pack(expand=True)

def abrir_menu_acoes(categoria):
    global categoria_atual
    categoria_atual = categoria
    esconder_todas_telas()
    
    for widget in frame_acoes.winfo_children():
        if widget.winfo_name() == "titulo_dinamico":
            widget.config(text=f"Menu {categoria}")
            
    frame_acoes.pack(expand=True)

def abrir_tela_inicial():
    esconder_todas_telas()
    frame_inicial.pack(expand=True)

def executar_acao(nome_acao):
    global categoria_atual
    esconder_todas_telas()
    frame_formulario.pack(expand=True)
    
    if categoria_atual == "Espécie":
        desenhar_formulario_especie(frame_formulario, nome_acao, lambda: abrir_menu_acoes("Espécie"), estilo_botao_menu, MARROM_PASTEL_ESCURO)
    elif categoria_atual == "Funcionário":
        desenhar_formulario_funcionario(frame_formulario, nome_acao, lambda: abrir_menu_acoes("Funcionário"), estilo_botao_menu, MARROM_PASTEL_ESCURO)
    elif categoria_atual == "Plantas":
        desenhar_formulario_plantas(frame_formulario, nome_acao, lambda: abrir_menu_acoes("Plantas"), estilo_botao_menu, MARROM_PASTEL_ESCURO)
    elif categoria_atual == "Sensor":
        desenhar_formulario_sensor(frame_formulario, nome_acao, lambda: abrir_menu_acoes("Sensor"), estilo_botao_menu, MARROM_PASTEL_ESCURO)

# --- MONTAGEM DOS CONTEÚDOS ---
frame_inicial = criar_tela_inicio(janela, abrir_menu_opcoes, estilo_botao_menu, MARROM_PASTEL_ESCURO)
frame_opcoes = criar_menu_opcoes(janela, abrir_menu_acoes, abrir_tela_inicial, estilo_botao_menu, MARROM_PASTEL_ESCURO)
frame_acoes = criar_menu_acoes(janela, executar_acao, abrir_menu_opcoes, estilo_botao_menu, MARROM_PASTEL_ESCURO)

# Inicializa o app
abrir_tela_inicial()
janela.mainloop()