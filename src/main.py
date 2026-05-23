import json
import os
import time

from leitor_csv import carregar_dados_cvs
from motor_imagem import desenhar_nome_centralizado, carregar_assets
from exportador import exportar_certificado
from envio_email import disparar_email
from validador import validar_insumos

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
    

def iniciar_geracao(callback_progresso=None):
    """
    Função principal que vai orquestrar as chamadas do sistema.
    """
    print("--- INICIANDO MOTOR DE CERTIFICADOS IEEE ---")

    config = configuracoes()
    if not config:
        print("[FALHA] Encerrando execução por falta de insumos.")
        return
    
    sucesso, mensagem = validar_insumos(config, DIRETORIO_RAIZ)
    if not sucesso:
        print(f"\n[ERRO] {mensagem}")
        return

    infos = config['configuracoes_certificado']
    img_base = os.path.join(DIRETORIO_RAIZ, infos['arquivos']['imagem_base'])
    fonte_path = os.path.join(DIRETORIO_RAIZ, infos['arquivos']['fonte_nome'])
    planilha = os.path.join(DIRETORIO_RAIZ, infos['arquivos']['planilha_dados'])
    tam_fonte = infos['fonte']['tamanho']
    pasta_saida = os.path.join(DIRETORIO_RAIZ, infos['arquivos'].get('pasta_saida', 'certificados_prontos'))
    pos_y = infos['posicao_nome']['y']

    participantes = carregar_dados_cvs(planilha)
    imagem_base, fonte = carregar_assets(img_base, fonte_path, tam_fonte)

    total = len(participantes)
    print(f"\n[STATUS] Processando {total} certificados...")

    # AQUI ESTÁ A MUDANÇA NO LOOP:
    for i, aluno in enumerate(participantes, 1):
        nome = aluno['nome']
        copia_imagem = imagem_base.copy()
        imagem_pronta = desenhar_nome_centralizado(copia_imagem, nome, fonte, pos_y)
        exportar_certificado(imagem_pronta, nome, pasta_saida)
        copia_imagem.close()

        # Avisa a interface que terminou um
        if callback_progresso:
            callback_progresso(i, total)

    print(f"\n[SUCESSO] Processo de geração concluído.")
    
    # Envio de e-mails
    disparar_email(participantes, pasta_saida)
        
if __name__ == "__main__":
    iniciar_geracao()