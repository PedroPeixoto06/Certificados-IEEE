from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Optional

def carregar_assets(caminho_imagem: str, caminho_fonte: str, tamanho_fonte: int = 60) -> Tuple[Image.Image, Optional[ImageFont.FreeTypeFont]]:
    """
    Carrega o template base do certificado em memória uma única vez para otimização de I/O.
    
    Args:
        caminho_imagem (str): Caminho absoluto para a imagem de fundo do certificado.
        caminho_fonte (str): Caminho da fonte (não instanciada aqui devido ao dimensionamento dinâmico).
        tamanho_fonte (int, opcional): Tamanho base, mantido por compatibilidade de assinatura.

    Returns:
        Tuple[Image.Image, None]: Retorna a imagem aberta em memória e None para o objeto de fonte.
    """
    imagem_base = Image.open(caminho_imagem)
    return imagem_base, None


def desenhar_nome_centralizado(imagem_copia: Image.Image, nome: str, caminho_fonte: str, tamanho_base: int, altura_y_fixa: int) -> Image.Image:
    """
    Processa a inserção do texto no certificado aplicando tipografia responsiva.
    Calcula a altura de face (Cap Height) para normalizar diferentes famílias tipográficas 
    e reduz a escala da fonte dinamicamente para evitar transbordamento nas margens horizontais.

    Args:
        imagem_copia (Image.Image): Instância em memória do template base.
        nome (str): Nome do participante a ser renderizado.
        caminho_fonte (str): Caminho absoluto do arquivo da fonte (.ttf ou .otf).
        tamanho_base (int): Altura visual alvo em pixels exigida pela interface.
        altura_y_fixa (int): Coordenada vertical onde a base do texto será ancorada.

    Returns:
        Image.Image: Template final com o nome corretamente dimensionado e posicionado.
    """
    draw = ImageDraw.Draw(imagem_copia)
    largura_imagem = imagem_copia.width
    
    # Restringe a área útil de texto a 66% da largura total do template para preservar margens de respiro
    largura_maxima = largura_imagem * 0.66
    
    # --- NORMALIZAÇÃO TIPOGRÁFICA ---
    # Utiliza um caractere maiúsculo sem descendentes ("A") para medir o 'Cap Height' real.
    # Isso impede que fontes cursivas sejam espremidas injustamente devido a letras com "pernas" longas (ex: g, y, j).
    tamanho_teste = 100 
    fonte_teste = ImageFont.truetype(caminho_fonte, tamanho_teste)
    
    bbox_teste = draw.textbbox((0, 0), "A", font=fonte_teste)
    altura_real_pixels = bbox_teste[3] - bbox_teste[1]
    
    # Calibração via regra de três para alinhar a altura física com a altura visual solicitada
    if altura_real_pixels > 0:
        fator_escala = tamanho_base / altura_real_pixels
        tamanho_ideal = int(tamanho_teste * fator_escala)
    else:
        tamanho_ideal = int(tamanho_base)
        
    tamanho_atual = tamanho_ideal
    fonte_atual = ImageFont.truetype(caminho_fonte, tamanho_atual)
    
    # --- PROTEÇÃO CONTRA TRANSBORDAMENTO (OVERFLOW) ---
    bbox = draw.textbbox((0, 0), nome, font=fonte_atual)
    largura_texto = bbox[2] - bbox[0]
    
    # Trava de segurança: a fonte pode encolher, mas nunca ficar menor que 30% da sua escala ideal ou 10pt
    tamanho_minimo = max(10, int(tamanho_ideal * 0.3))
    
    # Reduz iterativamente a fonte até que o nome se encaixe na margem de 66%
    while largura_texto > largura_maxima and tamanho_atual > tamanho_minimo:
        tamanho_atual -= 2
        fonte_atual = ImageFont.truetype(caminho_fonte, tamanho_atual)
        
        bbox = draw.textbbox((0, 0), nome, font=fonte_atual)
        largura_texto = bbox[2] - bbox[0]
    
    # --- RENDERIZAÇÃO ---
    eixo_x_centro = largura_imagem / 2
    
    # anchor="ms" garante que o texto expanda simetricamente a partir do centro (m) e sente exatamente sobre o eixo Y (s)
    draw.text((eixo_x_centro, altura_y_fixa), nome, font=fonte_atual, fill="black", anchor="ms")
    
    return imagem_copia