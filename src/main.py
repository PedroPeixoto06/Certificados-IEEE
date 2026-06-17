import json
import os
import sys
from typing import Dict, Any, Optional, Callable

from leitor_csv import carregar_dados_cvs
from motor_imagem import desenhar_nome_centralizado, carregar_assets
from exportador import exportar_certificado
from envio_email import disparar_email
from validador import validar_insumos

# --- RESOLUÇÃO DINÂMICA DE DIRETÓRIOS (COMPATIBILIDADE PYINSTALLER) ---
# Executáveis autônomos extraem seus arquivos em diretórios temporários em tempo de execução.
# Este bloco intercepta o contexto de execução para garantir o mapeamento de caminhos relativos robustos.
if getattr(sys, 'frozen', False):
    DIRETORIO_ATUAL = os.path.join(sys._MEIPASS, "src")
    DIRETORIO_RAIZ = sys._MEIPASS
    DIRETORIO_EXECUTAVEL = os.path.dirname(sys.executable)
else:
    DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
    DIRETORIO_RAIZ = os.path.dirname(DIRETORIO_ATUAL)
    DIRETORIO_EXECUTAVEL = DIRETORIO_RAIZ


def configuracoes() -> Optional[Dict[str, Any]]:
    """
    Carrega e decodifica as diretrizes de layout e automação mapeadas no arquivo JSON.

    Busca prioritariamente o arquivo externo gerado dinamicamente pela interface gráfica
    junto ao binário executável. Caso não encontre, recorre ao arquivo base embutido na raiz.

    Returns:
        Optional[Dict[str, Any]]: Dicionário com mapeamentos estruturais se decodificado com sucesso,
        ou None em caso de falha de leitura ou sintaxe inválida.
    """
    caminho_externo = os.path.join(DIRETORIO_EXECUTAVEL, "config.json")
    caminho_interno = os.path.join(DIRETORIO_RAIZ, "config.json")

    caminho_arquivo = caminho_externo if os.path.exists(caminho_externo) else caminho_interno

    if not os.path.exists(caminho_arquivo):
        print(f"[ERRO] Arquivo de configuração '{caminho_arquivo}' não encontrado.")
        return None
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            config: Dict[str, Any] = json.load(arquivo)
            return config
            
    except json.JSONDecodeError:
        print(f"[ERRO] Falha de sintaxe ao decodificar o arquivo JSON '{caminho_arquivo}'.")
        return None
    

def iniciar_geracao(
    callback_progresso: Optional[Callable[[int, int], None]] = None, 
    email_remetente: Optional[str] = None, 
    senha_remetente: Optional[str] = None
) -> None:
    """
    Gerencia o fluxo ponta a ponta de emissão: valida os insumos, consome os dados da
    planilha limpa, delega a renderização responsiva e dispara os lotes de e-mails de saída.

    Args:
        callback_progresso (Optional[Callable[[int, int], None]]): Função injetada da UI para 
            receber o incremento do passo atual em relação ao teto de passos projetado.
        email_remetente (Optional[str]): Credencial corporativa utilizada para autenticação SMTP.
        senha_remetente (Optional[str]): Senha de aplicativo de 16 dígitos fornecida pelo provedor.

    Raises:
        RuntimeError: Aborta a execução caso arquivos vitais estejam ausentes ou corrompidos.
    """
    print("--- INICIANDO MOTOR DE CERTIFICADOS IEEE ---")

    config = configuracoes()
    if not config:
        raise RuntimeError("Arquivo de configuração não encontrado ou inválido.")
    
    sucesso, mensagem = validar_insumos(config, DIRETORIO_RAIZ)
    if not sucesso:
        raise RuntimeError(mensagem)

    infos = config['configuracoes_certificado']
    img_base = os.path.join(DIRETORIO_RAIZ, infos['arquivos']['imagem_base'])
    fonte_path = os.path.join(DIRETORIO_RAIZ, infos['arquivos']['fonte_nome'])
    planilha = os.path.join(DIRETORIO_RAIZ, infos['arquivos']['planilha_dados'])
    tam_fonte = infos.get('fonte', {}).get('tamanho', 40)

    nome_da_pasta = infos['arquivos'].get('pasta_saida', 'certificados_prontos')
    pasta_saida = os.path.join(DIRETORIO_EXECUTAVEL, nome_da_pasta)

    pos_y = infos['posicao_nome']['y']

    participantes = carregar_dados_cvs(planilha)
    if not participantes:
        raise RuntimeError("A planilha não contém participantes válidos. Verifique se as colunas 'Nome' e 'Email' existem e estão preenchidas corretamente.")
        
    # Carrega a imagem base apenas uma vez na memória para alta performance
    imagem_base, _ = carregar_assets(img_base, fonte_path, tam_fonte)

    # --- MÉTRICA DE PROGRESSO ---
    total_alunos = len(participantes)
    total_passos = total_alunos * 2 
    
    print(f"\n[STATUS] Gerando {total_alunos} certificados...")

    for i, aluno in enumerate(participantes, 1):
        nome = aluno['nome']
        copia_imagem = imagem_base.copy()
        
        # O motor matemático se encarrega de reduzir a fonte para nomes excessivamente longos
        imagem_pronta = desenhar_nome_centralizado(copia_imagem, nome, fonte_path, tam_fonte, pos_y)
        
        exportar_certificado(imagem_pronta, nome, pasta_saida)
        copia_imagem.close()

        # Atualiza a barra de progresso da interface gráfica
        if callback_progresso:
            callback_progresso(i, total_passos)

    print("\n[SUCESSO] Processo de geração de PDFs concluído.")
    
    # --- INTEGRAÇÃO COM MÓDULO DE E-MAIL ---
    if email_remetente and senha_remetente:
        print("[STATUS] Iniciando disparo de e-mails em lote...")
        disparar_email(participantes, pasta_saida, email_remetente, senha_remetente, callback_progresso, total_passos)
    else:
        print("[AVISO] Credenciais não fornecidas. Os e-mails não serão enviados.")

if __name__ == "__main__":
    iniciar_geracao()