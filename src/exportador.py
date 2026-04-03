# src/exportador.py

from PIL import Image
import os


def exportar_certificado(imagem: Image.Image, nome: str, pasta_saida: str = "certificados") -> str:
    """
    Recebe uma imagem PIL pronta e a exporta como PDF com nome dinâmico.

    Args:
        imagem:      Objeto PIL.Image com o certificado já desenhado.
        nome:        Nome do aluno (usado para nomear o ficheiro).
        pasta_saida: Directório onde os PDFs serão guardados (criado se não existir).

    Returns:
        Caminho completo do ficheiro PDF gerado.
    """
    # Garante que a pasta de saída existe
    os.makedirs(pasta_saida, exist_ok=True)

    # Sanitiza o nome para uso seguro em nomes de ficheiro
    nome_sanitizado = nome.strip().replace(" ", "_")

    # Monta o nome dinâmico do ficheiro
    nome_ficheiro = f"Certificado_{nome_sanitizado}.pdf"
    caminho_completo = os.path.join(pasta_saida, nome_ficheiro)

    # Converte para RGB (necessário para salvar como PDF com Pillow)
    imagem_rgb = imagem.convert("RGB")

    # Guarda fisicamente o ficheiro em formato PDF
    imagem_rgb.save(caminho_completo, format="PDF", resolution=150)

    print(f"[OK] Certificado gerado: {caminho_completo}")
    return caminho_completo
