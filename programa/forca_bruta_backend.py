import time
import string
import itertools
import csv
from datetime import datetime

caracteres_possiveis = string.ascii_letters + string.digits + string.punctuation
tempo_por_tentativa = 0

def estimativas(senha_correta):
    base = len(caracteres_possiveis)
    comprimento = len(senha_correta)
    combinacoes_totais = sum(base ** i for i in range(1, comprimento + 1))
    tempo_maximo_estimado = combinacoes_totais * tempo_por_tentativa
    return combinacoes_totais, tempo_maximo_estimado

def forca_bruta(senha_correta, callback_progress=None):
    inicio = time.time()
    tentativas = 0
    tentativa_certa = ""
    encontrada = False

    base = len(caracteres_possiveis)
    comprimento = len(senha_correta)
    combinacoes_totais = sum(base ** i for i in range(1, comprimento + 1))
    contador_local = 0

    for tamanho in range(1, 100):  #limite de segurança
        for tentativa in itertools.product(caracteres_possiveis, repeat=tamanho):
            senha_tentativa = ''.join(tentativa)
            tentativas += 1
            contador_local += 1

            if callback_progress:
                progresso = min(100, int((tentativas / combinacoes_totais) * 100))
                callback_progress(progresso)

            if senha_tentativa == senha_correta:
                fim = time.time()
                tempo_total = fim - inicio
                tentativa_certa = senha_tentativa
                encontrada = True
                break

        if encontrada:
            break

    tempo_total = time.time() - inicio

    return {
        "senha": tentativa_certa,
        "tentativas": tentativas,
        "tempo": tempo_total,
        "tempo_maximo": combinacoes_totais * tempo_por_tentativa
    }

def salvar_csv(senha, tentativa, tentativas, tempo_gasto, tempo_maximo):
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    arquivo_csv = "relatorio_forca_bruta.csv"
    with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Data/Hora", "Senha Correta", "Tentativa Encontrada", "Tentativas", "Tempo Gasto (s)", "Tempo Máximo Estimado (s)"])
        writer.writerow([agora, senha, tentativa, tentativas, f"{tempo_gasto:.2f}", f"{tempo_maximo:.2f}"])
    return arquivo_csv