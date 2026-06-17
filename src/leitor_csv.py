import csv
import os
import sys
from typing import List, Dict

def carregar_dados_cvs(caminho_arquivo: str) -> List[Dict[str, str]]:
    """
    Lê e sanitiza os dados de participantes a partir de um arquivo CSV.
    Implementa normalização de cabeçalhos para evitar quebras do motor por 
    variações de digitação humana (ex: 'Nome', 'NOME', ' email ').

    Args:
        caminho_arquivo (str): Caminho absoluto ou relativo para a planilha de dados.

    Returns:
        List[Dict[str, str]]: Uma lista de dicionários contendo chaves normalizadas 
        ('nome' e 'email') e os respectivos dados limpos. Retorna lista vazia em caso de falha.
    """
    participantes: List[Dict[str, str]] = []
    
    if not os.path.exists(caminho_arquivo):
        print(f"[ERRO] A planilha de dados '{caminho_arquivo}' não foi encontrada.")
        return participantes

    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
            leitor_bruto = csv.reader(arquivo)
            
            try:
                cabecalhos_originais = next(leitor_bruto)
            except StopIteration:
                print("[ERRO] O arquivo CSV está completamente vazio.")
                return participantes
            
            # Normalização matemática das chaves para garantir case-insensitivity na extração
            cabecalhos_limpos = [str(c).strip().lower() for c in cabecalhos_originais]
            
            leitor_csv = csv.DictReader(arquivo, fieldnames=cabecalhos_limpos)
            
            for linha in leitor_csv:
                nome = linha.get('nome')
                email = linha.get('email')
                
                if nome and email:
                    nome_limpo = nome.strip()
                    email_limpo = email.strip()
                    
                    # Bloqueio estrutural contra linhas órfãs (ex: linhas que contêm apenas vírgulas vazias)
                    if nome_limpo and email_limpo:
                        participantes.append({
                            'nome': nome_limpo,
                            'email': email_limpo
                        })
                        
    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha na leitura do arquivo CSV: {e}")
        
    return participantes


# =================================================================================
# BLOCO DE TESTE ISOLADO
# Executado apenas se este arquivo for rodado diretamente (não afeta a interface gráfica)
# =================================================================================
if __name__ == "__main__":
    # Fallback automático para a nossa nova estrutura de pastas
    caminho_teste = sys.argv[1] if len(sys.argv) > 1 else "data/dados_teste.csv"
    
    print("--- AMBIENTE DE TESTE: LEITOR CSV ---")
    print(f"Buscando planilha em: {caminho_teste}\n")
    
    dados_teste = carregar_dados_cvs(caminho_teste)
    
    if dados_teste:
        print(f"[SUCESSO] {len(dados_teste)} registros válidos extraídos e sanitizados.")
        print("Amostra dos dados carregados:")
        
        # Imprime apenas os 3 primeiros para não poluir o terminal
        for p in dados_teste[:3]: 
            print(f" - {p['nome']} <{p['email']}>")
            
        if len(dados_teste) > 3:
            print(" ... (lista truncada para exibição)")
    else:
        print("[AVISO] Nenhum dado extraído. Verifique o arquivo CSV.")