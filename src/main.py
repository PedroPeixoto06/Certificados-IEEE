import json
import os
# As importações abaixo serão usadas na Fase 2
# from PIL import Image, ImageDraw, ImageFont 
# import pandas as pd

# Descobre o caminho da pasta raiz do projeto (uma pasta atrás da src/)
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_RAIZ = os.path.dirname(DIRETORIO_ATUAL)

def configuracoes(caminho_arquivo="config.json"):
    """
    Lê o arquivo JSON e retorna um dicionário com os parâmetros de configuração.
    Isso blinda o código contra valores hardcoded.
    """

    caminho_arquivo = os.path.join(DIRETORIO_RAIZ, "config.json")

    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo de configuração '{caminho_arquivo}' não encontrado.")
        return None
    
    try:
        with open(caminho_arquivo, 'r', encoding = 'utf-8') as arquivo:
            config = json.load(arquivo)
            return config
            
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo JSON '{caminho_arquivo}'. Verifique a sintaxe.")
        return None
    
def iniciar_geracao():
    """
    Função principal que vai orquestrar as chamadas do sistema.
    """
    print("--- INICIANDO MOTOR DE CERTIFICADOS IEEE ---")

    # 1. Carregar Insumos (Fase 1)
    config = configuracoes()

    if not config:
        print("[FALHA] Encerrando execução por falta de insumos.")

    # Extraindo as variáveis para facilitar o uso da equipe na Fase 2
    infos = config['configuracoes_certificado']
    
    img_base = os.path.join(DIRETORIO_RAIZ, infos['arquivos']['imagem_base'])
    fonte = os.path.join(DIRETORIO_RAIZ, infos['arquivos']['fonte_nome'])
    planilha = os.path.join(DIRETORIO_RAIZ, infos['arquivos']['planilha_dados'])
    
    pos_x = infos['posicao_nome']['x']
    pos_y = infos['posicao_nome']['y']

    print(f"\n[INFO] Parâmetros lidos com sucesso:")
    print(f" -> Imagem Base: {img_base}")
    print(f" -> Fonte Oficial: {fonte}")
    print(f" -> Coordenadas de Injeção: X={pos_x}, Y={pos_y}")
    print(f" -> Planilha Alvo: {planilha}\n")

    # 2. Espaço reservado para a Fase 2 (A injeção do Pillow entrará aqui)
    print("[STATUS] Aguardando implementação da Fase 2 (Leitura do CSV e Pillow)...")

if __name__ == "__main__":
    iniciar_geracao()
