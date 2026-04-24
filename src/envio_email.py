import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import dotenv
from dotenv import load_dotenv

# ==============================================================================
# DEMANDA 1: INFRAESTRUTURA E AUTENTICAÇÃO (Caio e Yasmin)
# Objetivo: Carregar as variáveis do .env e criar a conexão segura com o Google.
# ==============================================================================
# TODO (Caio/Yasmin): Importar o dotenv (load_dotenv).
# TODO (Caio/Yasmin): Ler as variáveis EMAIL_REMETENTE e SENHA_REMETENTE.

load_dotenv()

EMAIL_REMETENTE  = os.getenv("email_user")
SENHA_REMETENTE  = os.getenv("senha_user")

def disparar_email(lista_alunos, pasta_certificados):
    print("="*50)
    print("[INÍCIO] INICIANDO MOTOR DE ENVIO DE EMAILS")
    print("="*50)

    # TODO (Caio/Yasmin): Instanciar smtplib.SMTP na porta 587.
    # TODO (Caio/Yasmin): Executar starttls() e fazer o login.
    # servidor_smtp = ...

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
        servidor_smtp.send_message(msg) #checar o nome postumo do objeto 'msg'
        print(f"[ENVIADO] E-mail entregue com sucesso para {email_aluno}")



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
