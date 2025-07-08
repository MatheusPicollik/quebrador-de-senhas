import time
import string
import itertools

#caracteres permitidos: letras e números
caracteres_possiveis = string.ascii_letters + string.digits  # A-Z, a-z, 0-9

#senha do usuário
senha_correta = input("digite uma senha de 4 caracteres: ")

#verifica se a senha tem 4 caracteres
while len(senha_correta) != 4:
    senha_correta = input("senha invalida. digite uma senha de exatamente 4 caracteres: ")

print("\niniciando ataque por força bruta\n")

tentativas = 0

#gera todas as combinações possíveis de 4 caracteres
for tentativa in itertools.product(caracteres_possiveis, repeat=4):
    senha_tentativa = ''.join(tentativa)
    print(f"tentando: {senha_tentativa}")
    tentativas += 1

    if senha_tentativa == senha_correta:
        print(f"\nsenha encontrada: {senha_tentativa} após {tentativas} tentativas.")
        break