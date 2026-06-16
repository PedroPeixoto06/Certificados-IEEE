from PIL import Image, ImageDraw, ImageFont

def carregar_assets(caminho_imagem, caminho_fonte, tamanho_fonte=60):
    """Abre a imagem base uma única vez (alta performance)."""
    imagem_base = Image.open(caminho_imagem)
    # Deixamos o retorno da fonte como None porque ela será gerada dinamicamente por aluno
    return imagem_base, None

def desenhar_nome_centralizado(imagem_copia, nome, caminho_fonte, tamanho_base, altura_y_fixa):
    """Pega numa cópia limpa da imagem, reduz a fonte se o nome for gigante e centraliza o texto."""
    # 1. Cria a caneta EXCLUSIVA para esta cópia
    draw = ImageDraw.Draw(imagem_copia)
    
    # 2. Descobre os limites horizontais da imagem
    largura_imagem = imagem_copia.width
    # Define uma margem de segurança de 72% da largura total para o texto nunca encostar nas bordas
    largura_maxima = largura_imagem * 0.72
    
    # =================================================================================
    # 3. NORMALIZAÇÃO TIPOGRÁFICA (O fim das fontes pequenas!)
    # =================================================================================
    # Medimos uma "string de referência" que tem letras altas e baixas
    string_referencia = "A" 
    tamanho_teste = 100 
    fonte_teste = ImageFont.truetype(caminho_fonte, tamanho_teste)
    
    # Descobre a altura real do corpo principal da letra em píxeis
    bbox_teste = draw.textbbox((0, 0), string_referencia, font=fonte_teste)
    altura_real_pixels = bbox_teste[3] - bbox_teste[1]
    
    # Regra de três: calibra a fonte para que o 'A' atinja a altura desejada
    if altura_real_pixels > 0:
        fator_escala = tamanho_base / altura_real_pixels
        tamanho_ideal = int(tamanho_teste * fator_escala)
    else:
        tamanho_ideal = int(tamanho_base)
        
    # Inicializa a fonte com o novo tamanho perfeitamente calibrado
    tamanho_atual = tamanho_ideal
    fonte_atual = ImageFont.truetype(caminho_fonte, tamanho_atual)
    
    # 4. Calcula a largura do texto em píxeis usando a bounding box (caixa de envelope)
    bbox = draw.textbbox((0, 0), nome, font=fonte_atual)
    largura_texto = bbox[2] - bbox[0]
    
    # 5. Loop de redução: se o nome for maior que a margem, encolhe de 2 em 2 pontos
    # Define um tamanho mínimo dinâmico (nunca menor que 30% do tamanho ideal)
    tamanho_minimo = max(10, int(tamanho_ideal * 0.3))
    
    while largura_texto > largura_maxima and tamanho_atual > tamanho_minimo:
        tamanho_atual -= 2
        fonte_atual = ImageFont.truetype(caminho_fonte, tamanho_atual)
        
        # Recalcula a largura com o novo tamanho menor
        bbox = draw.textbbox((0, 0), nome, font=fonte_atual)
        largura_texto = bbox[2] - bbox[0]
    
    # 6. Descobre o centro horizontal exato da imagem automaticamente
    eixo_x_centro = largura_imagem / 2
    
    # 7. Desenha o texto usando ancoragem matemática do Pillow
    # 'm' (Middle): Centraliza o texto horizontalmente a partir do eixo_x_centro
    # 's' (Baseline): Apoia a base das letras exatamente em cima da altura_y_fixa
    draw.text((eixo_x_centro, altura_y_fixa), nome, font=fonte_atual, fill="black", anchor="ms")
    
    # Devolve a imagem pronta para ser exportada
    return imagem_copia