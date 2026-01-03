import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import secrets
import string

load_dotenv()

""" 
Organização:  
Estrutura o e-mail em partes bem definidas, seguindo o padrão MIME (Multipurpose Internet Mail Extensions).
→ Isso garante que qualquer cliente de e-mail (Gmail, Outlook, Thunderbird, etc.) consiga interpretar."""
class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_username)

    def enviar_email(self, destinatario, assunto, corpo_html):

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = assunto
            msg['From'] = self.from_email
            msg['To'] = destinatario
            part = MIMEText(corpo_html, 'html')
            msg.attach(part)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username,self.smtp_password)
                server.send_message(msg)

            print(f'Email enviado para{destinatario}')
            return True

        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False    
    
    def gerar_codigo (self, tamanho = 6):
        caracteres = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(caracteres) for _ in range(tamanho))
    
    def criar_email_recuperacao(self, nome_usuario, codigo):

        return f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Recuperação de Senha</h2>
                <p>Olá {nome_usuario},</p>
                <p>Recebemos uma solicitação para redefinir sua senha.</p>
                <p>Seu código de verificação é: <strong>{codigo}</strong></p>
                <p>Este código expira em 15 minutos.</p>
                <p>Se você não solicitou esta alteração, ignore este email.</p>
                <br>
                <p>Atenciosamente,<br>Equipe do Sistema</p>
            </body>
        </html>
        """

email_service = EmailService()