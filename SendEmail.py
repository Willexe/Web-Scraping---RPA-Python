import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# Configurações para construção do email
def enviar_email_com_anexo(sender, password, recipient, subject, body, arquivos=None):
    if arquivos is None:
        arquivos = []
    server_smtp = "smtp.gmail.com" # Nesse caso está configurado para Gmail caso o seu seja diferente procurar SMTP e a port referente ao seu email
    port = 587

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = ", ".join(recipient)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Anexo
    for caminho in arquivos:
        with open(caminho, 'rb') as f:
            parte = MIMEApplication(f.read(), name=caminho)
            parte['Content-Disposition'] = f'attachment; filename="{caminho}"'
            msg.attach(parte)

    try:
        server = smtplib.SMTP(server_smtp, port)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        print("E-mail enviado com anexo com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
