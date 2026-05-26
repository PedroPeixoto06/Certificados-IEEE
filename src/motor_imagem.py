from PIL import Image, ImageDraw, ImageFont

def carregar_assets(caminho_imagem, caminho_fonte, tamanho_fonte=60):
    """Abre a imagem e a fonte uma única vez (alta performance)."""
    imagem_base = Image.open(caminho_imagem)
    fonte = ImageFont.truetype(caminho_fonte, tamanho_fonte)
    
    return imagem_base, fonte

def desenhar_nome_centralizado(imagem_copia, nome, fonte, altura_y_fixa):
    """Pega numa cópia limpa da imagem e desenha o nome perfeitamente ao centro."""
    # 1. Cria a caneta EXCLUSIVA para esta cópia
    draw = ImageDraw.Draw(imagem_copia)
    
    # 2. Descobre o centro horizontal exato da imagem automaticamente
    largura_imagem = imagem_copia.width
    eixo_x_centro = largura_imagem / 2
    
    # 3. Desenha o texto usando ancoragem matemática do Pillow
    # 'm' (Middle): Centraliza o texto horizontalmente a partir do eixo_x_centro
    # 's' (Baseline): Apoia a base das letras exatamente em cima da altura_y_fixa
    draw.text((eixo_x_centro, altura_y_fixa), nome, font=fonte, fill="black", anchor="ms")
    
    # Devolve a imagem pronta para ser exportada
    return imagem_copia