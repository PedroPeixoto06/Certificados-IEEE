import json
import os
import time

from leitor_csv import carregar_dados_cvs
from motor_imagem import desenhar_nome_centralizado, carregar_assets
from exportador import exportar_certificado

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
    fonte_path = os.path.join(DIRETORIO_RAIZ, infos['arquivos']['fonte_nome'])
    planilha = os.path.join(DIRETORIO_RAIZ, infos['arquivos']['planilha_dados'])
    tam_fonte = infos['fonte']['tamanho']
    nome_da_pasta = infos['arquivos'].get('pasta_saida', 'certificados_prontos')
    pasta_saida = os.path.join(DIRETORIO_RAIZ, nome_da_pasta)
    
    pos_x = infos['posicao_nome']['x']
    pos_y = infos['posicao_nome']['y']

    print(f"\n[INFO] Parâmetros lidos com sucesso:")
    print(f" -> Imagem Base: {img_base}")
    print(f" -> Fonte Oficial: {fonte_path}")
    print(f" -> Coordenadas de Injeção: X={pos_x}, Y={pos_y}")
    print(f" -> Planilha Alvo: {planilha}\n")

    print(f'\n [DADOS] Lendo: {infos["arquivos"]["planilha_dados"]}')
    participantes = carregar_dados_cvs(planilha)

    if not participantes:
        print("[FALHA] Nenhum participante encontrado na planilha.")
        return
    
    print(f"[ASSETS] Carregando imagem e fonte...")

    try:
        imagem_base, fonte = carregar_assets(img_base, fonte_path, tam_fonte)

    except Exception as e:
        print(f'[ERRO] Falha ao carregar os assets: {e}')
        return

    print(f"\n[STATUS] Processando {len(participantes)} certificados...")
    tempo_inicio = time.time()

    for aluno in participantes:
        nome = aluno['nome']

        copia_imagem = imagem_base.copy()

        imagem_pronta = desenhar_nome_centralizado(copia_imagem, nome, fonte, pos_y)

        exportar_certificado(imagem_pronta, nome, pasta_saida)

        copia_imagem.close()

        duracao = round(time.time() - tempo_inicio, 2)

        print("\n" + "=" * 50)
        print(f"[SUCESSO] CONCLUIDO EM {duracao} segundos")
        print(f"[DIRETORIO] CERTIFICADOS EM: {pasta_saida}")
        print("=" * 50)
if __name__ == "__main__":
    iniciar_geracao()