from environs import Env
import smtplib
import time
import imaplib
import email
import os

env = Env()
env.read_env()

MY_EMAIL = env('GMAIL_USERNAME')
MY_PASSWORD = env('GMAIL_APP_PASSWORD')

IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993

def download_mytaxi_files(attachment_dir, search_year):
    print(f'Downloading receipts from Gmail for {search_year}...')
    mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    mail.login(MY_EMAIL, MY_PASSWORD)
    mail.select("mytaxi")
    search_string = f'(SINCE 01-Jan-{search_year})'
    _, data = mail.search(None, search_string)
    for num in data[0].split():
        _, data = mail.fetch(num, '(RFC822)' )
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()
            if bool(fileName):
                filePath = os.path.join(attachment_dir, fileName)
                if not os.path.isfile(filePath) :
                    print("Saving", fileName)
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                else:
                    print("Skipping", fileName)
    print('Download complete!')