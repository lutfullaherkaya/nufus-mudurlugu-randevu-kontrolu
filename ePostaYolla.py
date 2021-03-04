import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import datetime
import ePostalariOku


# https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development


# bunlari degistiriniz. sender maili gmail varsayarak yazdim kodu
SENDER_EMAIL = "email@email.com"
RECEIVER_EMAIL = "email@email.com"
PASSWORD = "password"

def stringYolla(string, baslik="Randevu Doluluk Oranı", 
        sender_email=SENDER_EMAIL, receiver_email=RECEIVER_EMAIL, password=PASSWORD):
    message = MIMEMultipart("alternative")
    message["Subject"] = baslik
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = "Sürücü belgesi randevusu için " +string
    html = """\
    <html>
        <body>
        Sürücü belgesi randevusu için """ + string + """\  
        </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
                sender_email, receiver_email, message.as_string()
        )
    
def capkaYollaVeCevabiDon(capkaAdresi, baslik="capka",
        sender_email=SENDER_EMAIL, receiver_email=RECEIVER_EMAIL, password=PASSWORD):
    dosyaAdi = os.path.basename(capkaAdresi)

    message = MIMEMultipart("alternative")
    message["Subject"] = baslik
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Resim"""
    html = """\
    <html>
        <body>
                Sa insan. Bir robot olarak şu capkçaça'yı okuyamadım: <br>
                <img src="cid:0">
                <br> Sürücü belgesi randevusunu kontrol etmek için lazım. Okuyup yazar mısın? Okuyamazsan "tekrar yolla reis" yazman yeterli. Hemen tekrar yollarım. Yanlış bir sayı yollama ama, o zaman çökebilir programım. 4 saatte bir kontrol edip posta atacağım sana.
        </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    with open(capkaAdresi, 'rb') as f:
        # set attachment mime and file name, the image type is png
        mime = MIMEBase('image', 'png', filename=dosyaAdi)
        # add required header data:
        mime.add_header('Content-Disposition', 'attachment', filename=dosyaAdi)
        mime.add_header('X-Attachment-Id', '0')
        mime.add_header('Content-ID', '<0>')
        # read attachment file content into the MIMEBase object
        mime.set_payload(f.read())
        # encode with base64
        encoders.encode_base64(mime)
        # add MIMEBase object to MIMEMultipart object
        message.attach(mime)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        gondermeTarihi = datetime.datetime.now() + datetime.timedelta(0,5)
        server.sendmail(
                sender_email, receiver_email, message.as_string()
        )
    
    cevap = ePostalariOku.sonEPostayiOkuCapcaDon(gondermeTarihi)
    return cevap[:4]