import time
import string
import itertools
from numba import cuda
import numpy as np

# ----- CONFIGURAÇÃO -----
caracteres_possiveis = string.ascii_letters + string.digits + string.punctuation
senha_correta = input("Digite a senha: ")
assert 1 <= len(senha_correta) <= 6, "Senha deve ter entre 1 e 6 caracteres para evitar explosão combinatória"


senha_correta_ascii = np.array([ord(c) for c in senha_correta], dtype=np.uint8) #ERRO======ERRO======ERRO======ERRO======ERRO

threads_por_bloco = 256
tentativas_encontradas = cuda.to_device(np.zeros(1, dtype=np.int32))
senha_encontrada_gpu = cuda.to_device(np.zeros(len(senha_correta), dtype=np.uint8))


@cuda.jit
def kernel_forca_bruta(caracteres, senha_target, senha_len, offset, resultado, senha_encontrada):
    idx = cuda.grid(1)
    index_global = idx + offset
    base = len(caracteres)

   
    temp = index_global
    tentativa = cuda.local.array(16, dtype=uint8)

    for i in range(senha_len - 1, -1, -1):
        tentativa[i] = caracteres[temp % base]
        temp //= base

    
    match = True
    for i in range(senha_len):
        if tentativa[i] != senha_target[i]:
            match = False
            break

    if match:
        resultado[0] = 1
        for i in range(senha_len):
            senha_encontrada[i] = tentativa[i]


def main():
    inicio = time.time()

    base = len(caracteres_possiveis)
    senha_len = len(senha_correta)
    total_combinacoes = base ** senha_len

    print(f"Iniciando ataque GPU...")
    print(f"Total de combinações: {total_combinacoes:,}")

    caracteres_np = np.array([ord(c) for c in caracteres_possiveis], dtype=np.uint8)
    d_caracteres = cuda.to_device(caracteres_np)

    blocos_por_lote = 1024
    passo = threads_por_bloco * blocos_por_lote

    for offset in range(0, total_combinacoes, passo):
        if tentativas_encontradas.copy_to_host()[0] == 1:
            break

        kernel_forca_bruta[blocos_por_lote, threads_por_bloco](
            d_caracteres,
            senha_correta_ascii,
            senha_len,
            offset,
            tentativas_encontradas,
            senha_encontrada_gpu
        )

        cuda.synchronize()

    fim = time.time()

    if tentativas_encontradas.copy_to_host()[0] == 1:
        senha_bytes = senha_encontrada_gpu.copy_to_host()
        senha_final = ''.join([chr(c) for c in senha_bytes])
        print(f"\n✅ Senha encontrada: {senha_final}")
        print(f"⏱️ Tempo total: {fim - inicio:.2f} segundos")
    else:
        print("\n❌ Senha não encontrada dentro do limite definido.")

if __name__ == "__main__":
    main()