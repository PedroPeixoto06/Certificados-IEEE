import os
from dotenv import load_dotenv

def validar_insumos(config, diretorio_raiz):

    """
    Verifica se todos os pré-requisitos existem antes de iniciar a geração.
    Retorna (True, "OK") se tudo estiver certo, ou (False, "Mensagem de Erro").
    """

    print("[VALIDACAO] Checando pré-requisitos do sistema...")

    # 1. Validar as Chaves do .env
    caminho_env = os.path.join(diretorio_raiz, '.env')
    load_dotenv(caminho_env)

    email = os.getenv("email_user")
    senha = os.getenv("senha_user")

    if not email or not senha:
        return False, "Credenciais ausentes. O arquivo .env não possui 'email_user' ou 'senha_user'."
    
    # 2. Validar se a Fonte Existe
    infos = config.get("configuracoes_certificado", {})
    arquivos = infos.get("arquivos", {})

    fonte_path = os.path.join(diretorio_raiz, arquivos.get("fonte_nome", ""))
    if not os.path.isfile(fonte_path):
        return False, f"Arquivo de fonte não encontrado: {fonte_path}"
    
    # 3. Validar a Imagem Base
    img_base = os.path.join(diretorio_raiz, arquivos.get("imagem_base", ""))
    if not os.path.isfile(img_base):
        return False, f"Arquivo de imagem base não encontrado: {img_base}"
    
    # 4. Validar se o CSV existe e NÃO está vazio
    planilha_path = os.path.join(diretorio_raiz, arquivos.get("planilha_dados", ""))
    if not os.path.isfile(planilha_path):
        return False, f"Planilha de dados não encontrada: {planilha_path}"
    
    # Checa o tamanho do arquivo para garantir que não está vazio (apenas com o cabeçalho)
    # Um arquivo CSV vazio ou só com "nome,email" tem menos de 15 bytes geralmente

    if os.path.getsize(planilha_path) < 15:
        return False, f"Planilha de dados está vazia ou sem participantes: {planilha_path}"
    
    return True, "[OK] Todos os pré-requisitos foram validados com sucesso."