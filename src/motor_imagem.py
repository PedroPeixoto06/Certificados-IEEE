from PIL import Image, ImageDraw, ImageFont

def desenhar_nome_centralizado(draw, nome, fonte, largura_imagem, altura_y_fixa):
    # Calculando a bounding box do texto
    bbox = draw.textbbox((0, 0), nome, font=fonte)
    
    largura_texto = bbox[2] - bbox[0]
    
    # Fórmula da centralização para o Eixo X
    eixo_x_dinamico = (largura_imagem - largura_texto) / 2
    
    # Desenha o texto na posição calculada
    draw.text((eixo_x_dinamico, altura_y_fixa), nome, font=fonte, fill="black")
    
    return eixo_x_dinamico

