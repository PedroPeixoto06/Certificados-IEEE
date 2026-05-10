from PIL import Image, ImageDraw, ImageFont

def carregar_assets(caminho_imagem, caminho_fonte, tamanho_fonte=60):
    """Abre a imagem e a fonte uma única vez (alta performance)."""
    imagem_base = Image.open(caminho_imagem)
    fonte = ImageFont.truetype(caminho_fonte, tamanho_fonte)
    
    return imagem_base, fonte

def desenhar_nome_centralizado(imagem_copia, nome, fonte, altura_y_fixa):
    """Pega numa cópia limpa da imagem e desenha o nome ao centro."""
    # 1. Cria a caneta EXCLUSIVA para esta cópia
    draw = ImageDraw.Draw(imagem_copia)
    
    # 2. Descobre a largura total da imagem automaticamente
    largura_imagem = imagem_copia.width
    
    # 3. Calcula o Bounding Box e a centralização (Matemática do Bruno)
    bbox = draw.textbbox((0, 0), nome, font=fonte)
    largura_texto = bbox[2] - bbox[0]
    eixo_x_dinamico = (largura_imagem - largura_texto) / 2
    
    # 4. Desenha o texto na posição calculada
    draw.text((eixo_x_dinamico, altura_y_fixa), nome, font=fonte, fill="black")
    
    # Devolve a imagem pronta para ser exportada
    return imagem_copia