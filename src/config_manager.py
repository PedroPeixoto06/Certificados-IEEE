# src/config_manager.py

import json
import os
from typing import Callable


# Caminho canônico do arquivo de configuração do projeto
CAMINHO_CONFIG = "config.json"

# Estrutura padrão garantida caso o arquivo ainda não exista
CONFIG_PADRAO = {
    "caminho_planilha": "",
    "caminho_template": "",
    "caminho_fonte": "",
    "pasta_saida": "certificados_prontos",
    "modo_pausa": "humano",
    "segundos_pausa": 3
}


# ─────────────────────────────────────────────
#  LEITURA
# ─────────────────────────────────────────────

def carregar_config() -> dict:
    """
    Lê o config.json e devolve um dicionário com as configurações atuais.
    Se o arquivo não existir, cria um com os valores padrão.
    """
    if not os.path.exists(CAMINHO_CONFIG):
        salvar_config(CONFIG_PADRAO)
        return CONFIG_PADRAO.copy()

    with open(CAMINHO_CONFIG, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Garante que novas chaves padrão existam mesmo em configs antigas
    for chave, valor in CONFIG_PADRAO.items():
        dados.setdefault(chave, valor)

    return dados


# ─────────────────────────────────────────────
#  ESCRITA
# ─────────────────────────────────────────────

def salvar_config(novos_valores: dict) -> None:
    """
    Reescreve o config.json com os valores fornecidos.
    Faz merge com os dados existentes — só sobrescreve o que for passado.

    Args:
        novos_valores: Dicionário com as chaves a atualizar.
    """
    config_atual = carregar_config() if os.path.exists(CAMINHO_CONFIG) else CONFIG_PADRAO.copy()
    config_atual.update(novos_valores)

    with open(CAMINHO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config_atual, f, ensure_ascii=False, indent=4)

    print(f"[CONFIG] config.json atualizado: {list(novos_valores.keys())}")


# ─────────────────────────────────────────────
#  BINDS — Captura de escolhas da UI
# ─────────────────────────────────────────────

def bind_planilha(caminho: str) -> None:
    """Bind do botão 'Selecionar Planilha' da Tamiris."""
    salvar_config({"caminho_planilha": caminho})


def bind_template(caminho: str) -> None:
    """Bind do botão 'Selecionar Template' da Tamiris."""
    salvar_config({"caminho_template": caminho})


def bind_salvar_e_gerar(
    caminho_planilha: str,
    caminho_template: str,
    iniciar_geracao: Callable,
    callback_progresso: Callable[[int, str], None] | None = None
) -> None:
    """
    Bind do botão principal 'Gerar Certificados'.

    1. Persiste todas as escolhas da UI no config.json.
    2. Aciona a função iniciar_geracao() do motor.

    Args:
        caminho_planilha:    Caminho capturado do campo da UI.
        caminho_template:    Caminho capturado do campo da UI.
        iniciar_geracao:     Função do motor (main.py) a ser acionada.
        callback_progresso:  Função opcional da UI para atualizar
                             barra/contador de progresso (Tarefa 4 do Pedro).
    """
    # 1. Persiste as escolhas no config.json
    salvar_config({
        "caminho_planilha": caminho_planilha,
        "caminho_template": caminho_template,
    })

    # 2. Dispara o motor, injetando o callback de progresso se existir
    if callback_progresso:
        iniciar_geracao(callback_progresso=callback_progresso)
    else:
        iniciar_geracao()