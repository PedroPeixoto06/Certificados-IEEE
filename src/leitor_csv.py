import csv
import os

def carregar_dados_cvs(caminho_arquivo):
    """
    Lê um arquivo CSV e retorna uma lista de dicionários contendo nomes e e-mails.
    Suporta cabeçalhos em qualquer variação de caixa (ex: Nome, nome, NOME, Email, email).
    """
    participantes = []
    
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo {caminho_arquivo} não foi encontrado.")
        return participantes

    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
            # 1. Captura a primeira linha de forma bruta para tratar os cabeçalhos
            leitor_bruto = csv.reader(arquivo)
            try:
                cabecalhos_originais = next(leitor_bruto)
            except StopIteration:
                print("Erro: O arquivo CSV está completamente vazio.")
                return participantes
            
            # Sanitização: Remove espaços extras e força tudo para letras minúsculas
            cabecalhos_limpos = [str(c).strip().lower() for c in cabecalhos_originais]
            
            # 2. Continua a leitura usando os cabeçalhos padronizados em minúsculo
            leitor_csv = csv.DictReader(arquivo, fieldnames=cabecalhos_limpos)
            
            for linha in leitor_csv:
                # Agora a busca é feita sempre em minúsculo, independente de como estava no arquivo
                nome = linha.get('nome')
                email = linha.get('email')
                
                if nome and email:
                    nome_limpo = nome.strip()
                    email_limpo = email.strip()
                    
                    # Evita adicionar linhas em branco ou cabeçalhos duplicados acidentalmente
                    if nome_limpo and email_limpo:
                        participantes.append({
                            'nome': nome_limpo,
                            'email': email_limpo
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