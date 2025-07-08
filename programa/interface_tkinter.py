import tkinter as tk
from tkinter import ttk, messagebox
import threading
from forca_bruta_backend import forca_bruta, estimativas, salvar_csv

def iniciar_ataque():
    senha = entry.get()
    if not senha:
        messagebox.showerror("Erro", "Digite uma senha.")
        return

    iniciar_btn.config(state=tk.DISABLED)
    progresso_bar["value"] = 0
    resultado_text.delete(1.0, tk.END)

    def atualizar_progresso(valor):
        progresso_bar["value"] = valor

    def rodar():
        combinacoes, tempo_max = estimativas(senha)
        resultado_text.insert(tk.END, f"Senha alvo: {senha}\n")
        resultado_text.insert(tk.END, f"Combinações estimadas: {combinacoes:,}\n")
        resultado_text.insert(tk.END, f"Tempo máximo estimado: {tempo_max:.2f} segundos\n\n")

        resultado = forca_bruta(senha, callback_progress=atualizar_progresso)

        resultado_text.insert(tk.END, f"\nSenha encontrada: {resultado['senha']}\n")
        resultado_text.insert(tk.END, f"Tentativas: {resultado['tentativas']}\n")
        resultado_text.insert(tk.END, f"Tempo gasto: {resultado['tempo']:.2f} segundos\n")

        csv_path = salvar_csv(
            senha, resultado["senha"], resultado["tentativas"],
            resultado["tempo"], resultado["tempo_maximo"]
        )
        resultado_text.insert(tk.END, f"\nRelatório salvo: {csv_path}")
        iniciar_btn.config(state=tk.NORMAL)

    threading.Thread(target=rodar, daemon=True).start()

root = tk.Tk()
root.title("Ataque de Força Bruta - GUI")
root.geometry("700x500")

tk.Label(root, text="Digite a senha:", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(root, font=("Arial", 12), show="*", width=40)
entry.pack()

iniciar_btn = tk.Button(root, text="Iniciar Força Bruta", font=("Arial", 12), bg="#2e86de", fg="white", command=iniciar_ataque)
iniciar_btn.pack(pady=10)

progresso_bar = ttk.Progressbar(root, length=500, mode='determinate')
progresso_bar.pack(pady=5)

resultado_text = tk.Text(root, height=20, font=("Consolas", 10), wrap=tk.WORD)
resultado_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()