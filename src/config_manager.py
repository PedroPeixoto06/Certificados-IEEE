import json
import os
from typing import Dict, Any, Optional, Callable

# Caminho canônico para o arquivo de persistência de configurações
CAMINHO_CONFIG = "config.json"

# Dicionário de fallback estrutural para inicialização de novos ambientes
CONFIG_PADRAO: Dict[str, Any] = {
    "caminho_planilha": "",
    "caminho_template": "",
    "caminho_fonte": "",
    "pasta_saida": "certificados_prontos",
    "modo_pausa": "humano",
    "segundos_pausa": 3
}


# ──────────────────────────────────────────────────────────────────────────────
#  MÓDULO DE LEITURA (I/O)
# ──────────────────────────────────────────────────────────────────────────────

def carregar_config() -> Dict[str, Any]:
    """
    Recupera as diretrizes de configuração salvas em disco. Caso o arquivo 
    JSON não exista, inicializa o arquivo com a estrutura padrão.

    Returns:
        Dict[str, Any]: Mapeamento atualizado contendo os parâmetros de execução.
    """
    if not os.path.exists(CAMINHO_CONFIG):
        salvar_config(CONFIG_PADRAO)
        return CONFIG_PADRAO.copy()

    with open(CAMINHO_CONFIG, "r", encoding="utf-8") as f:
        dados: Dict[str, Any] = json.load(f)

    # Injeção preventiva: garante a retrocompatibilidade inserindo chaves novas
    # caso o usuário esteja rodando uma versão antiga do arquivo JSON
    for chave, valor in CONFIG_PADRAO.items():
        dados.setdefault(chave, valor)

    return dados


# ──────────────────────────────────────────────────────────────────────────────
#  MÓDULO DE ESCRITA (I/O)
# ──────────────────────────────────────────────────────────────────────────────

def salvar_config(novos_valores: Dict[str, Any]) -> None:
    """
    Atualiza o arquivo de configuração em disco realizando uma operação de mesclagem 
    (merge) não destrutiva, preservando os campos não informados.

    Args:
        novos_valores (Dict[str, Any]): Subconjunto de chaves e valores a serem atualizados.
    """
    config_atual = carregar_config() if os.path.exists(CAMINHO_CONFIG) else CONFIG_PADRAO.copy()
    config_atual.update(novos_valores)

    with open(CAMINHO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config_atual, f, ensure_ascii=False, indent=4)

    print(f"[CONFIG] Parâmetros persistidos em disco: {list(novos_valores.keys())}")


# ──────────────────────────────────────────────────────────────────────────────
#  MÓDULO DE VÍNCULOS (BINDS DE INTERFACE)
# ──────────────────────────────────────────────────────────────────────────────

def bind_planilha(caminho: str) -> None:
    """
    Registra imediatamente no JSON o caminho da planilha selecionada na interface.

    Args:
        caminho (str): Rota do arquivo de dados extraído.
    """
    salvar_config({"caminho_planilha": caminho})


def bind_template(caminho: str) -> None:
    """
    Registra imediatamente no JSON o caminho do template visual selecionado na interface.

    Args:
        caminho (str): Rota do arquivo de imagem base.
    """
    salvar_config({"caminho_template": caminho})


def bind_salvar_e_gerar(
    caminho_planilha: str,
    caminho_template: str,
    caminho_fonte: str,
    iniciar_geracao: Callable[..., None],
    posicao_y: int = 500,
    callback_progresso: Optional[Callable[[int, int], None]] = None,
    email_remetente: str = "",
    senha_remetente: str = ""
) -> None:
    """
    Valida, estrutura e aninha os dados em lote recolhidos da interface gráfica,
    atualiza o arquivo de configuração global e despacha a execução imediata do motor.

    Args:
        caminho_planilha (str): Caminho para o arquivo de participantes.
        caminho_template (str): Caminho para a imagem de fundo do certificado.
        caminho_fonte (str): Caminho para a família tipográfica (.ttf/.otf).
        iniciar_geracao (Callable[..., None]): Função orquestradora importada do módulo main.
        posicao_y (int, opcional): Coordenada vertical para fixação do texto. Padrão é 500.
        callback_progresso (Optional[Callable[[int, int], None]]): Função de atualização de progresso da UI.
        email_remetente (str, opcional): Credencial de e-mail em memória.
        senha_remetente (str, opcional): Token de segurança de aplicativo em memória.
    """
    config_atual = carregar_config()
    
    # Assegura a integridade do nó aninhado estrutural para os insumos gráficos
    if "configuracoes_certificado" not in config_atual:
        config_atual["configuracoes_certificado"] = {"arquivos": {}, "posicao_nome": {}}
        
    config_atual["configuracoes_certificado"]["arquivos"]["planilha_dados"] = caminho_planilha
    config_atual["configuracoes_certificado"]["arquivos"]["imagem_base"] = caminho_template
    config_atual["configuracoes_certificado"]["arquivos"]["fonte_nome"] = caminho_fonte
    
    # Injeção estrutural segura para o eixo de ancoragem vertical
    if "posicao_nome" not in config_atual["configuracoes_certificado"]:
        config_atual["configuracoes_certificado"]["posicao_nome"] = {}
    config_atual["configuracoes_certificado"]["posicao_nome"]["y"] = posicao_y

    with open(CAMINHO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config_atual, f, ensure_ascii=False, indent=4)

    print(f"[CONFIG] Estrutura de metadados de lote sincronizada. Invocando o maestro principal...")

    # Aciona o fluxo principal repassando as dependências de progresso e e-mail
    iniciar_geracao(
        callback_progresso=callback_progresso,
        email_remetente=email_remetente,
        senha_remetente=senha_remetente
    )