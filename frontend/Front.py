import tkinter as tk
from tkinter import *

janela = tk.Tk()
janela.title("Janela Principal")
janela.geometry("1100x700")

label = tk.Label(janela, text="Bem-vindo à Janela Principal!")
label.pack(pady=20)

# Botao para abrir a janela secundária
botao = tk.Button(janela, text="Abrir Janela Secundária", command=lambda: janela_secundaria())
botao.pack(pady=10)

canvas = tk.Canvas(janela, width=1100, height=700, bg="blue")
canvas.create_rectangle(50, 50, 200, 200, fill="blue")

texto = Text(janela, height=1, width=40)
texto.insert(INSERT, "digite sua senha")
texto.pack()

conteudo = texto.get("1.0", END)
print (conteudo)

janela.mainloop()