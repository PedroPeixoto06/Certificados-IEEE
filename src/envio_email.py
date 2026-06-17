import os
import time
import smtplib
import random
from typing import List, Dict, Optional, Callable
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def criar_pacote_email(nome_aluno: str, email_destino: str, email_remetente: str) -> MIMEMultipart:
    """
    Constrói o envelope SMTP e o corpo HTML do e-mail.

    Args:
        nome_aluno (str): Nome do participante para personalização do texto.
        email_destino (str): Endereço de destino.
        email_remetente (str): Endereço institucional do remetente autenticado.

    Returns:
        MIMEMultipart: Objeto de e-mail montado, pronto para receber anexos e ser despachado.
    """
    msg = MIMEMultipart()
    
    msg['From'] = email_remetente
    msg['To'] = email_destino
    msg['Subject'] = f"Certificado Disponível: {nome_aluno} - Evento IEEE"

    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: auto; border: 1px solid #004a99; border-radius: 10px; overflow: hidden;">
                <div style="background-color: #004a99; color: white; padding: 20px; text-align: center;">
                    <h1 style="margin: 0;">Parabéns, {nome_aluno}!</h1>
                </div>
                <div style="padding: 20px;">
                    <p>Olá!</p>
                    <p>É com grande alegria que o <b>IEEE Student Branch UFC</b> disponibiliza o seu certificado.</p>
                    <p>O documento está anexado a este e-mail em formato PDF.</p>
                    <p style="background-color: #f4f4f4; padding: 10px; border-left: 5px solid #004a99;">
                        Agradecemos a sua participação!
                    </p>
                </div>
                <div style="background-color: #eee; padding: 10px; text-align: center; font-size: 12px; color: #666;">
                    Equipe de Projetos IEEE UFC
                </div>
            </div>
        </body>
    </html>
    """

    corpo_email = MIMEText(html, 'html')
    msg.attach(corpo_email)
    return msg


def aguardar_entre_envios(modo: str = "fixo", segundos: int = 3) -> None:
    """
    Implementa uma taxa de limitação (Rate Limiting) para prevenir bloqueios 
    por heurística de Spam dos provedores de e-mail.
    """
    if modo == "humano":
        pausa = round(random.uniform(3.0, 6.0), 2)
        print(f" ⏳ Pausa humanizada: {pausa}s...")
        time.sleep(pausa)
    else:
        print(f" Aguardando {segundos}s antes do próximo envio...")
        time.sleep(segundos)


def disparar_email(
    lista_alunos: List[Dict[str, str]], 
    pasta_certificados: str, 
    email_remetente: str, 
    senha_remetente: str, 
    callback_progresso: Optional[Callable[[int, int], None]] = None, 
    total_passos: int = 0
) -> None:
    """
    Orquestra o lote de envios de e-mail, gerenciando a conexão segura SMTP (TLS),
    a anexação binária dos PDFs com codificação UTF-8 e os logs de resiliência.
    """
    print("="*50)
    print("[INÍCIO] INICIANDO MOTOR DE ENVIO DE EMAILS")
    print("="*50)

    # Abre a conexão segura SMTP (TLS) usando as credenciais passadas via interface
    servidor_smtp = smtplib.SMTP("smtp.gmail.com", 587)
    servidor_smtp.ehlo()
    servidor_smtp.starttls() 
    servidor_smtp.ehlo()
    servidor_smtp.login(email_remetente, senha_remetente)

    total_alunos = len(lista_alunos)

    for i, aluno in enumerate(lista_alunos, 1):
        nome_aluno = aluno['nome']
        email_aluno = aluno['email']

        try:
            print(f"[PROCESSANDO] Preparando envio para {nome_aluno} ({email_aluno})")

            msg = criar_pacote_email(nome_aluno, email_aluno, email_remetente)
            
            nome_sanitizado = nome_aluno.strip().replace(" ", "_")
            nome_arquivo = f"Certificado_{nome_sanitizado}.pdf"
            caminho_pdf = os.path.join(pasta_certificados, nome_arquivo)
            
            # Anexação Binária (Base64) do arquivo PDF
            with open(caminho_pdf, "rb") as arquivo:
                parte = MIMEBase("application", "octet-stream")
                parte.set_payload(arquivo.read())
            
            encoders.encode_base64(parte)
            
            # Força a codificação UTF-8 no nome do anexo para suportar acentuação no download
            parte.add_header(
                "Content-Disposition",
                "attachment",
                filename=("utf-8", "", nome_arquivo)
            )
            msg.attach(parte)
            
            servidor_smtp.send_message(msg)
            print(f"[ENVIADO] E-mail entregue com sucesso para {email_aluno}")

            aguardar_entre_envios(modo="humano")

            if callback_progresso:
                passo_atual = total_alunos + i
                callback_progresso(passo_atual, total_passos)

        except Exception as e:
            # Resiliência: Grava o erro em disco sem derrubar o loop principal
            with open('erros_envio.txt', 'a', encoding='utf-8') as f_erro:
                f_erro.write(f"Falha ao enviar para {nome_aluno} ({email_aluno}) | Erro: {str(e)}\n")
            
            print(f"[ERRO] Falha no envio para {nome_aluno}. Erro registrado em 'erros_envio.txt'. Pulando para o próximo...")
            continue

    servidor_smtp.quit()
    print("\n[SUCESSO] Lote de disparos finalizado e conexão SMTP encerrada.")