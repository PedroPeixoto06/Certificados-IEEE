import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ==============================================================================
# DEMANDA 1: INFRAESTRUTURA E AUTENTICAÇÃO (Caio e Yasmin)
# Objetivo: Carregar as variáveis do .env e criar a conexão segura com o Google.
# ==============================================================================
# TODO (Caio/Yasmin): Importar o dotenv (load_dotenv).
# TODO (Caio/Yasmin): Ler as variáveis EMAIL_REMETENTE e SENHA_REMETENTE.

def disparar_email(lista_alunos, pasta_certificados):
    print("="*50)
    print("[INÍCIO] INICIANDO MOTOR DE ENVIO DE EMAILS")
    print("="*50)

    # TODO (Caio/Yasmin): Instanciar smtplib.SMTP na porta 587.
    # TODO (Caio/Yasmin): Executar starttls() e fazer o login.
    # servidor_smtp = ...

    # Loop principal de envio para cada aluno da planilha
    for aluno in lista_alunos:
        nome_aluno = aluno['nome']
        email_aluno = aluno['email']

        # ==============================================================================
        # DEMANDA 5: RESILIÊNCIA E LOGS
        # Objetivo: Envolver o processo num Try/Except para o sistema não quebrar.
        # ==============================================================================
        # TODO: Iniciar o bloco 'try:' aqui.

        print(f"[PROCESSANDO] Montando certificado para {nome_aluno} ({email_aluno})")


        # ==============================================================================
        # DEMANDA 2: COMPOSIÇÃO ESTRUTURADA MIME
        # Objetivo: Criar o "envelope", o Assunto e o Corpo do e-mail em HTML.
        # ==============================================================================
        # TODO: Criar o objeto msg = MIMEMultipart().
        # TODO: Definir msg['From'], msg['To'] e msg['Subject'].
        # TODO: Criar o corpo em HTML e anexar com MIMEText.

def criar_pacote_email(nome_aluno, email_destino):

    msg = MIMEMultipart()
    
    msg['From'] = "IEEE Student Branch UFC <email-IEEE@gmail.com>"  #colcar o email do ramo que vai enviar os certificados
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


        # ==============================================================================
        # DEMANDA 3: ANEXAÇÃO DINÂMICA
        # Objetivo: Encontrar o PDF do aluno em modo binário e anexar ao envelope.
        # ==============================================================================
        # TODO: Montar o caminho exato do arquivo PDF.
        # TODO: Abrir o PDF em modo 'rb' (leitura binária).
        # TODO: Usar MIMEBase, aplicar payload, encodar em Base64 e anexar à 'msg'.
        # TODO: Fechar o arquivo PDF da memória.


        # --- DISPARO EFETIVO (Caio/Yasmin) ---
        # TODO (Caio/Yasmin): Usar o servidor_smtp para enviar a 'msg' montada pelo Pedro e Juan.
        # servidor_smtp.send_message(msg)


        # ==============================================================================
        # DEMANDA 4: CONTROLE ANTIBLOQUEIO 
        # Objetivo: Fazer o script "respirar" entre envios para evitar punição de Spam.
        # ==============================================================================
        # TODO: Usar time.sleep() para criar uma pausa de 3 a 5 segundos.
        # TODO: Adicionar um print informando o tempo de espera.


        # TODO (Continuação da Demanda 5): 
        # Criar o bloco 'except Exception as e:'. 
        # Abrir 'relatorio_erros.txt' em modo 'a', escrever a falha.
        # Usar o comando 'continue' para pular para o próximo aluno.

    # TODO (Caio/Yasmin): Fechar a conexão SMTP com servidor_smtp.quit() no final de tudo.
    print("\n[SUCESSO] Linha de disparo finalizada.")
