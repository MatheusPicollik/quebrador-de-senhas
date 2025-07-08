import time
import string
import itertools
import csv
from datetime import datetime
from threading import Thread, Event
from queue import Queue

# ----- CONFIGURAÇÃO -----
tempo_por_tentativa = 0.0005
num_threads = 8              
caracteres_possiveis = string.ascii_letters + string.digits + string.punctuation
# -------------------------

senha_correta = input("Digite a senha (qualquer número de caracteres, incluindo especiais): ")
while len(senha_correta) == 0:
    senha_correta = input("Senha inválida. Digite uma senha não vazia: ")

base = len(caracteres_possiveis)
comprimento = len(senha_correta)
combinacoes_totais = sum(base ** i for i in range(1, comprimento + 1))
tempo_maximo_estimado = combinacoes_totais * tempo_por_tentativa

print(f"\nIniciando ataque por força bruta com {num_threads} threads...")
print(f"Tentativas máximas esperadas: {combinacoes_totais:,}")
print(f"Tempo máximo estimado: {tempo_maximo_estimado:.2f} segundos ({tempo_maximo_estimado/60:.2f} minutos)\n")

senha_encontrada_event = Event()
fila_tentativas = Queue()
resultado = {
    'tentativa_certa': '',
    'tentativas': 0,
    'tempo_total': 0.0
}


def worker():
    while not senha_encontrada_event.is_set():
        try:
            tentativa = fila_tentativas.get(timeout=1)
        except:
            continue

        senha_tentativa = ''.join(tentativa)
        resultado['tentativas'] += 1

        if senha_tentativa == senha_correta:
            resultado['tentativa_certa'] = senha_tentativa
            senha_encontrada_event.set()
            break

        time.sleep(tempo_por_tentativa)

        fila_tentativas.task_done()


def gerar_combinacoes():
    for tamanho in range(1, 100):
        for tentativa in itertools.product(caracteres_possiveis, repeat=tamanho):
            if senha_encontrada_event.is_set():
                return
            fila_tentativas.put(tentativa)


inicio = time.time()


threads = [Thread(target=worker) for _ in range(num_threads)] #ERRO======ERRO======ERRO======ERRO======ERRO
for t in threads:
    t.start()


gerar_combinacoes()


fila_tentativas.join()
fim = time.time()


resultado['tempo_total'] = fim - inicio


print(f"\nSenha encontrada: '{resultado['tentativa_certa']}'")
print(f"Tentativas realizadas: {resultado['tentativas']}")
print(f"Tempo total gasto: {resultado['tempo_total']:.2f} segundos ({resultado['tempo_total']/60:.2f} minutos)")


agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
arquivo_csv = "relatorio_forca_bruta_threads.csv"

with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    file.seek(0, 2) 
    if file.tell() == 0:
        writer.writerow(["Data/Hora", "Senha Correta", "Tentativa Encontrada", "Tentativas", "Tempo Gasto (s)", "Tempo Máximo Estimado (s)"])
    writer.writerow([
        agora,
        senha_correta,
        resultado['tentativa_certa'],
        resultado['tentativas'],
        f"{resultado['tempo_total']:.2f}",
        f"{tempo_maximo_estimado:.2f}"
    ])

print(f"\nRelatório salvo em: {arquivo_csv}")