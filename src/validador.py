import os
from typing import Dict, Any, Tuple

def validar_insumos(config: Dict[str, Any], diretorio_raiz: str) -> Tuple[bool, str]:
    """
    Verifica a integridade e a existência dos arquivos essenciais (fonte, template e dados)
    antes de delegar a execução para o motor de geração.

    Args:
        config (Dict[str, Any]): Dicionário contendo as configurações mapeadas do JSON.
        diretorio_raiz (str): Caminho absoluto do diretório principal do projeto.

    Returns:
        Tuple[bool, str]: Uma tupla contendo o status da validação (True/False) 
        e a respectiva mensagem de log detalhada.
    """
    print("[VALIDACAO] Checando pré-requisitos do sistema...")

    infos = config.get("configuracoes_certificado", {})
    arquivos = infos.get("arquivos", {})

    # Validação do arquivo de fonte tipográfica
    fonte_path = os.path.join(diretorio_raiz, arquivos.get("fonte_nome", ""))
    if not os.path.isfile(fonte_path):
        return False, f"Arquivo de fonte não encontrado: {fonte_path}"
    
    # Validação do template base do certificado
    img_base = os.path.join(diretorio_raiz, arquivos.get("imagem_base", ""))
    if not os.path.isfile(img_base):
        return False, f"Arquivo de imagem base não encontrado: {img_base}"
    
    # Validação da existência da planilha de dados
    planilha_path = os.path.join(diretorio_raiz, arquivos.get("planilha_dados", ""))
    if not os.path.isfile(planilha_path):
        return False, f"Planilha de dados não encontrada: {planilha_path}"
    
    # Evita o disparo do motor caso o arquivo contenha apenas o cabeçalho (menos de 15 bytes)
    if os.path.getsize(planilha_path) < 15:
        return False, f"Planilha de dados está vazia ou sem participantes: {planilha_path}"
    
    return True, "[OK] Todos os pré-requisitos foram validados com sucesso."