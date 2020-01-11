import smtplib
import time
import imaplib
import email
import os
from datetime import datetime
from environs import Env

env = Env()
env.read_env()

MY_EMAIL = env('GMAIL_USERNAME')
MY_PASSWORD = env('GMAIL_APP_PASSWORD')
IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993
CURRENT_YEAR = datetime.now().year
DEFAULT_SEARCH_STRING = f'(SINCE 01-Jan-{CURRENT_YEAR})' # can be replaced with 'ALL'

def download_mytaxi_files(attachment_dir, search_string=DEFAULT_SEARCH_STRING):
    print('Downloading receipts from Gmail...')
    mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    mail.login(MY_EMAIL, MY_PASSWORD)
    mail.select("mytaxi")
    type, data = mail.search(None, search_string)
    mail_ids = data[0]
    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)' )
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