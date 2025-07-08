import time
import string
import itertools
import csv
from datetime import datetime

#lista completa de caracteres permitidos
caracteres_possiveis = string.ascii_letters + string.digits + string.punctuation

#tempo estimado por tentativa (em segundos)
tempo_por_tentativa = 0.001

#solicita a senha
senha_correta = input("Digite a senha (qualquer número de caracteres, incluindo especiais): ")

#validação
while len(senha_correta) == 0:
    senha_correta = input("Senha inválida. Digite uma senha não vazia: ")

#cálculo do total de combinações possíveis até o comprimento da senha
base = len(caracteres_possiveis)
comprimento = len(senha_correta)
combinacoes_totais = sum(base ** i for i in range(1, comprimento + 1))
tempo_maximo_estimado = combinacoes_totais * tempo_por_tentativa

print(f"\nIniciando ataque por força bruta...")
print(f"Senha alvo: {senha_correta}")
print(f"Tentativas máximas esperadas: {combinacoes_totais:,}")
print(f"Tempo máximo estimado: {tempo_maximo_estimado:.2f} segundos ({tempo_maximo_estimado/60:.2f} minutos aprox.)\n")

# Início da contagem de tempo
inicio = time.time()
tentativas = 0
encontrada = False
tentativa_certa = ""

# Loop de tentativa
for tamanho in range(1, 100):  # Limite de segurança
    for tentativa in itertools.product(caracteres_possiveis, repeat=tamanho):
        senha_tentativa = ''.join(tentativa)
        tentativas += 1

        if senha_tentativa == senha_correta:
            fim = time.time()
            tempo_total = fim - inicio
            tentativa_certa = senha_tentativa
            encontrada = True
            break

        time.sleep(tempo_por_tentativa)

    if encontrada:
        break

# Mostra o resultado
print(f"\nSenha encontrada: '{tentativa_certa}'")
print(f"Tentativas realizadas: {tentativas}")
print(f"Tempo total gasto: {tempo_total:.2f} segundos ({tempo_total/60:.2f} minutos)")

# Gera o CSV
agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
arquivo_csv = "relatorio_forca_bruta.csv"

with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Data/Hora", "Senha Correta", "Tentativa Encontrada", "Tentativas", "Tempo Gasto (s)", "Tempo Máximo Estimado (s)"])
    writer.writerow([agora, senha_correta, tentativa_certa, tentativas, f"{tempo_total:.2f}", f"{tempo_maximo_estimado:.2f}"])

print(f"\nRelatório salvo em: {arquivo_csv}")