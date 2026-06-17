import os
from PIL import Image

def exportar_certificado(imagem: Image.Image, nome: str, pasta_saida: str = "certificados") -> str:
    """
    Exporta uma imagem em memória para um arquivo físico no formato PDF, 
    aplicando rotinas de sanitização no nome do arquivo de saída.

    Args:
        imagem (Image.Image): Instância do objeto PIL.Image contendo o certificado renderizado.
        nome (str): Nome do participante, utilizado como identificador do arquivo.
        pasta_saida (str, opcional): Diretório de destino para armazenamento dos PDFs. 
            Criado automaticamente caso não exista. O padrão é "certificados".

    Returns:
        str: Caminho absoluto ou relativo do arquivo PDF gerado em disco.
    """
    # Garante a existência do diretório de destino de forma segura contra concorrência
    os.makedirs(pasta_saida, exist_ok=True)

    # Substitui espaços por underscores para evitar quebras de caminho em URLs ou sistemas POSIX
    nome_sanitizado = nome.strip().replace(" ", "_")
    nome_arquivo = f"Certificado_{nome_sanitizado}.pdf"
    caminho_completo = os.path.join(pasta_saida, nome_arquivo)

    # O formato PDF exige estritamente o espaço de cores RGB (ou CMYK).
    # Caso a imagem base contenha transparência (RGBA), a conversão descarta o canal alpha
    # evitando uma exceção crítica do Pillow durante o salvamento.
    imagem_rgb = imagem.convert("RGB")

    # Persiste o arquivo com calibração de densidade de pixels estável para impressão básica
    imagem_rgb.save(caminho_completo, format="PDF", resolution=150)

    print(f"[OK] Certificado gerado com sucesso: {caminho_completo}")
    return caminho_completo
