import datetime

from email.utils import parsedate_tz
import time
import imaplib
import email
from email.header import decode_header
import webbrowser
import os

# https://www.thepythoncode.com/article/reading-emails-in-python

# account credentials
USERNAME = "mail@mail.com"
PASSWORD = "password"

def sonEPostayiOkuCapcaDon(soruTarihi, username=USERNAME, password=PASSWORD):
    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)

    # 30 dk boyunca 5sn de 1 cevap sorgulayacak
    i = 0
    while i < 360:
        status, messages = imap.select("INBOX")
        # number of top emails to fetch
        N = 1
        # total number of emails
        messages = int(messages[0])

        for i in range(messages, messages-N, -1):
            # fetch the email message by ID
            res, msg = imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])

                    tarih = parsedate_tz(msg["Date"])
                    cevapTarihi = datetime.datetime(
                        tarih[0], tarih[1], tarih[2], tarih[3], tarih[4], tarih[5])

                    if cevapTarihi > soruTarihi:
                        # decode the email subject
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            # if it's a bytes, decode to str
                            subject = subject.decode()
                        # decode email sender
                        From, encoding = decode_header(msg.get("From"))[0]
                        if isinstance(From, bytes):
                            From = From.decode(encoding)
                        # print("Subject:", subject)
                        # print("From:", From)
                        # if the email message is multipart (multipart mesela hem duz yazi hem html demekmis)
                        if msg.is_multipart():
                            # iterate over email parts
                            for part in msg.walk():
                                # extract content type of email
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    # get the email body
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    pass
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    # print text/plain emails and skip attachments
                                    return body
                                elif "attachment" in content_disposition:
                                    # download attachment
                                    filename = part.get_filename()
                                    if filename:
                                        if not os.path.isdir(subject):
                                            # make a folder for this email (named after the subject)
                                            os.mkdir(subject)
                                        filepath = os.path.join(subject, filename)
                                        # download attachment and save it
                                        open(filepath, "wb").write(part.get_payload(decode=True))
                        else:
                            # extract content type of email
                            content_type = msg.get_content_type()
                            # get the email body
                            body = msg.get_payload(decode=True).decode()
                            if content_type == "text/plain":
                                # print only text email parts
                                return body
                        if content_type == "text/html":
                            """
                            # if it's HTML, create a new HTML file and open it in browser
                            if not os.path.isdir(subject):
                                # make a folder for this email (named after the subject)
                                os.mkdir(subject)
                            filename = f"{subject[:50]}.html"
                            filepath = os.path.join(subject, filename)
                            # write the file
                            open(filepath, "w").write(body)
                            # open in the default browser
                            webbrowser.open(filepath)
                            """
                        print("="*100)
        time.sleep(5)
    
    # close the connection and logout
    imap.close()
    imap.logout()