import zipfile
import string
import itertools

#caminho do arquivo RAR
caminho_arquivo = "senha.zip"

#caracteres permitidos
caracteres = string.ascii_letters + string.digits + string.punctuation

def tentar_senha(senha_teste):
    try:
        with zipfile.ZipFile(caminho_arquivo) as zf:
            zf.extractall(pwd=senha_teste)
        return True
    except:
        return False

for tamanho in range(1, 6):  #até 5 caracteres
    for tentativa in itertools.product(caracteres, repeat=tamanho):
        senha = ''.join(tentativa)
        print(f"Tentando: {senha}")
        if tentar_senha(senha):
            print(f"\nSenha encontrada: {senha}")
            exit()

print("Senha não encontrada.")