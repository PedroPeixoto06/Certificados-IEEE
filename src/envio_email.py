import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import dotenv
from dotenv import load_dotenv
import random


# ==============================================================================
# CARREGAMENTO DE AMBIENTE
# ==============================================================================


load_dotenv()

EMAIL_REMETENTE  = os.getenv("email_user")
SENHA_REMETENTE  = os.getenv("senha_user")


# ==============================================================================
# FUNCOES DE APOIO
# ==============================================================================

def criar_pacote_email(nome_aluno, email_destino, email_remetente):

    """Demanda 2: Cria o envelope e o corpo HTML do e-mail."""

    msg = MIMEMultipart()
    
    msg['From'] = email_remetente
    msg['To'] = email_destino
    msg['Subject'] = f"Certificado Disponível: {nome_aluno} - evento IEEE"

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

    """Demanda 4: Freio antibloqueio para evitar punição de Spam."""

    if modo == "humano":
        pausa = round(random.uniform(3.0, 6.0), 2)
        print(f"  ⏳ Pausa humanizada: {pausa}s...")
        time.sleep(pausa)
    else:
        print(f"  Aguardando {segundos}s antes do próximo envio...")
        time.sleep(segundos)


# ==============================================================================
# MOTOR PRINCIPAL
# ==============================================================================


def disparar_email(lista_alunos, pasta_certificados):
    print("="*50)
    print("[INÍCIO] INICIANDO MOTOR DE ENVIO DE EMAILS")
    print("="*50)

    # 1. Abre a conexão segura SMTP
    servidor_smtp = smtplib.SMTP("smtp.gmail.com", 587) #abre uma conexão TCP com o servidor smtp.gmail.com na porta 587
    servidor_smtp.ehlo()
    servidor_smtp.starttls() 
    servidor_smtp.ehlo()
    servidor_smtp.login(EMAIL_REMETENTE, SENHA_REMETENTE)

    # Loop principal de envio para cada aluno da planilha
    for aluno in lista_alunos:
        nome_aluno = aluno['nome']
        email_aluno = aluno['email']


        # ==============================================================================
        # RESILIÊNCIA E LOGS
        # ==============================================================================
        

        try:
            print(f"[PROCESSANDO] Montando certificado para {nome_aluno} ({email_aluno})")

            # Demanda 2: Puxa o pacote criado pelo Pedro
            msg = criar_pacote_email(nome_aluno, email_aluno, EMAIL_REMETENTE)
            
            
            # ==============================================================================
            # DEMANDA 3: ANEXAÇÃO DINÂMICA
            # ==============================================================================
            
            #Anexa o PDF
            caminho_pdf = f"{pasta_certificados}/{nome_aluno}.pdf"
            with open(caminho_pdf, "rb") as arquivo:
                parte = MIMEBase("application", "octet-stream")
                parte.set_payload(arquivo.read())
            encoders.encode_base64(parte)
            parte.add_header(
                "Content-Disposition",
                f'attachment; filename="{nome_aluno}.pdf"'
            )
            msg.attach(parte)
            
            #Disparo Efetivo
            servidor_smtp.send_message(msg) #checar o nome postumo do objeto 'msg'
            print(f"[ENVIADO] E-mail entregue com sucesso para {email_aluno}")

            #Pausa entre envios para evitar bloqueio
            aguardar_entre_envios(modo="humano")

        except Exception as e:
                # Captura o erro para que o programa não seja interrompido
                with open('erros_envio.txt', 'a', encoding='utf-8') as f_erro:
                    f_erro.write(f"Falha ao enviar para {nome_aluno} ({email_aluno}) | Erro: {str(e)}\n")
                
                print(f"[ERRO] Falha no envio para {nome_aluno}. Erro registrado em erros_envio.txt. Pulando para o próximo...")
                continue
    #Finaliza a conexão após terminar todos os alunos
    servidor_smtp.quit()
    print("\n[SUCESSO] Linha de disparo finalizada.")
