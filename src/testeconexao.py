import os
import smtplib
import dotenv
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("email_user")
SENHA = os.getenv("senha_user")

try:
    print(f"Tentando conectar com: {EMAIL}...")
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.ehlo()
    servidor.starttls()  # Sua demanda de segurança
    servidor.ehlo()
    servidor.login(EMAIL, SENHA)
    print("[SUCESSO] Conexão e login realizados com sucesso!")
    servidor.quit()
except Exception as e:
    print(f"[FALHA] Erro na autenticação: {e}")
    print("Dica: Verifique se a 'Senha de App' está correta e se o .env usa os nomes 'email_user' e 'senha_user'.")