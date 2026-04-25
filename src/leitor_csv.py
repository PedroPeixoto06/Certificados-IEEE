import csv
import os

def carregar_dados_cvs(caminho_arquivo):
    """
    Lê um arquivo CSV e retorna uma lista de dicionários contendo nomes e e-mails.
    """
    participantes = []
    
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo {caminho_arquivo} não foi encontrado.")
        return participantes

    try:
        with open(caminho_arquivo, mode='r', encoding='latin-1') as arquivo:
            leitor_csv = csv.DictReader(arquivo)
            for linha in leitor_csv:
                # Extraindo nome e e-mail
                nome = linha.get('Nome')
                email = linha.get('Email')
                
                if nome and email:
                    participantes.append({
                        'nome': nome.strip(),
                        'email': email.strip()
                    })
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        
    return participantes

import sys

# --- ONDE VOCÊ ALTERA O CAMINHO ---
if __name__ == "__main__":
    
    # Se o usuário não passar um caminho, tenta usar 'data/dados.csv'
    
    if len(sys.argv) > 1:
        caminho = sys.argv[1]
    else:
        caminho = "data/dados.csv"
        print(f"Dica: Você pode rodar o script passando o caminho do arquivo.\nExemplo: python leitor_csv.py caminho/do/arquivo.csv\n")
    
    dados = carregar_dados_cvs(caminho)
    
    if dados:
        print(f"Sucesso! {len(dados)} participantes encontrados.")
        for p in dados:
            print(f"Nome: {p['nome']} | E-mail: {p['email']}")
    else:
        print("Nenhum dado carregado. Verifique o arquivo CSV.")

