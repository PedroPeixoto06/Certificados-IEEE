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
# INFRAESTRUTURA E AUTENTICAÇÃO
# Objetivo: Carregar as variáveis do .env e criar a conexão segura com o Google.
# ==============================================================================
# Importar o dotenv (load_dotenv).
# Ler as variáveis EMAIL_REMETENTE e SENHA_REMETENTE.

load_dotenv()

EMAIL_REMETENTE  = os.getenv("email_user")
SENHA_REMETENTE  = os.getenv("senha_user")

def disparar_email(lista_alunos, pasta_certificados):
    print("="*50)
    print("[INÍCIO] INICIANDO MOTOR DE ENVIO DE EMAILS")
    print("="*50)

    # Executar starttls() e fazer o login.
    # Instanciar smtplib.SMTP na porta 587.
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
        # RESILIÊNCIA E LOGS
        # Objetivo: Envolver o processo num Try/Except para o sistema não quebrar.
        # ==============================================================================
        # Iniciar o bloco 'try:' aqui.
        
        try:
            print(f"[PROCESSANDO] Montando certificado para {nome_aluno} ({email_aluno})")


        except Exception as e:
                # Captura o erro para que o programa não seja interrompido
                with open('erros_envio.txt', 'a', encoding='utf-8') as f_erro:
                    f_erro.write(f"Falha ao enviar para {nome_aluno} ({email_aluno}) | Erro: {str(e)}\n")
                
                print(f"[ERRO] Falha no envio para {nome_aluno}. Erro registrado em erros_envio.txt. Pulando para o próximo...")
                continue


        # ==============================================================================
        # COMPOSIÇÃO ESTRUTURADA MIME
        # Objetivo: Criar o "envelope", o Assunto e o Corpo do e-mail em HTML.
        # ==============================================================================
        #  Criar o objeto msg = MIMEMultipart().
        #  Definir msg['From'], msg['To'] e msg['Subject'].
        #  Criar o corpo em HTML e anexar com MIMEText.

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
        # TODO: Montar o caminho exato do arquivo PDF.
        # TODO: Abrir o PDF em modo 'rb' (leitura binária).
        # TODO: Usar MIMEBase, aplicar payload, encodar em Base64 e anexar à 'msg'.
        # TODO: Fechar o arquivo PDF da memória.


# --- DISPARO EFETIVO ---
# TODO (Caio/Yasmin): Usar o servidor_smtp para enviar a 'msg' montada pelo Pedro e Juan.
    
servidor_smtp.send_message(msg) #checar o nome postumo do objeto 'msg'
print(f"[ENVIADO] E-mail entregue com sucesso para {email_aluno}")



# ==============================================================================
# CONTROLE ANTIBLOQUEIO 
# Objetivo: Fazer o script "respirar" entre envios para evitar punição de Spam.
# ==============================================================================
# Usar time.sleep() para criar uma pausa de 3 a 5 segundos.
# Adicionar um print informando o tempo de espera.

def aguardar_entre_envios(modo: str = "fixo", segundos: int = 3) -> None:

#Injeta uma pausa estratégica entre os envios de e-mail para evitar
#bloqueio por comportamento de spam.

#Args:
#modo:     "fixo"    → pausa sempre igual (time.sleep(segundos))
#"humano"  → pausa aleatória entre 3 e 6s (mais natural)
#segundos: Duração base da pausa no modo "fixo" (padrão: 3).


    if modo == "humano":
        pausa = round(random.uniform(3.0, 6.0), 2)
        print(f"  ⏳ Pausa humanizada: {pausa}s...")
        time.sleep(pausa)
    else:
        print(f"  Aguardando {segundos}s antes do próximo envio...")
        time.sleep(segundos)


# TODO (Caio/Yasmin): Fechar a conexão SMTP com servidor_smtp.quit() no final de tudo.
print("\n[SUCESSO] Linha de disparo finalizada.")
