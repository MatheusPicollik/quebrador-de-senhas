import time
import string
import itertools

#lista completa de caracteres: letras, números e especiais
caracteres_possiveis = string.ascii_letters + string.digits + string.punctuation

#tempo estimado por tentativa (em segundos)
tempo_por_tentativa = 0

#senha do usuario
senha_correta = input("Digite a senha (qualquer número de caracteres, incluindo especiais): ")

#validação
while len(senha_correta) == 0:
    senha_correta = input("Senha inválida. Digite uma senha não vazia: ")

#calculo do total de combinações possíveis até o comprimento da senha
base = len(caracteres_possiveis)
comprimento = len(senha_correta)
combinacoes_totais = sum(base ** i for i in range(1, comprimento + 1))
tempo_maximo_estimado = combinacoes_totais * tempo_por_tentativa

print(f"\nIniciando ataque por força bruta...")
print(f"Senha alvo: {senha_correta}")
print(f"Tentativas máximas esperadas: {combinacoes_totais:,}")
print(f"Tempo máximo estimado: {tempo_maximo_estimado:.2f} segundos ({tempo_maximo_estimado/60:.2f} minutos aprox.)\n")

#inicia contagem de tempo real
inicio = time.time()
tentativas = 0
encontrada = False

for tamanho in range(1, 100):  #limite de segurança
    for tentativa in itertools.product(caracteres_possiveis, repeat=tamanho):
        senha_tentativa = ''.join(tentativa)
        tentativas += 1

        if senha_tentativa == senha_correta:
            fim = time.time()
            tempo_total = fim - inicio
            print(f"\nSenha encontrada: '{senha_tentativa}'")
            print(f"Tentativas realizadas: {tentativas}")
            print(f"Tempo total gasto: {tempo_total:.2f} segundos ({tempo_total/60:.2f} minutos)")
            encontrada = True
            break

        #tempo de espera
        time.sleep(tempo_por_tentativa)

    if encontrada:
        break