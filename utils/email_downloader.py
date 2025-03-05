import base64
import email
import imaplib
import os
from email.header import decode_header

from core.config import settings
from core.exceptions import NotFoundException, InvalidCredentialsException

EMAIL = settings.email_config.email
PASSWORD = settings.email_config.password
IMAP_SERVER = settings.email_config.imap_server
IMAP_PORT = settings.email_config.imap_port
SENDER_EMAIL = settings.email_config.sender_email
SUBJECT_KEYWORD = settings.email_config.subject_keyword

def email_auth(imap_server, imap_port, email, password):
    mail = imaplib.IMAP4_SSL(imap_server, imap_port)
    try:
        mail.login(email, password)
        mail.select("inbox")
        return mail, 'Auth successful'
    except imaplib.IMAP4.error:
        raise InvalidCredentialsException()



def encode_search_criteria(field, value):
    if any(ord(char) > 127 for char in value):
        encoded_value = base64.b64encode(value.encode('utf-8')).decode()
        value = f'=?UTF-8?B?{encoded_value}?='
    return f'{field} "{value}"'


def decode_mime_words(s):
    decoded_words = email.header.decode_header(s)
    return "".join(
        word.decode(encoding or "utf-8") if isinstance(word, bytes) else word
        for word, encoding in decoded_words
    )


def find_messages_via_search_criteria(mail):
    status, messages = mail.search(None, f'FROM "{SENDER_EMAIL}"')
    message_numbers = messages[-1].split()

    if not message_numbers:
        raise NotFoundException()

    return message_numbers


def download_message_attachments():
    mail = email_auth(imap_server=IMAP_SERVER,
                      imap_port=IMAP_PORT,
                      email=EMAIL,
                      password=PASSWORD)
    mail = mail[0]

    message_numbers = find_messages_via_search_criteria(mail)

    for num in message_numbers:
        status, data = mail.fetch(num, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = decode_mime_words(msg["Subject"])

        if SUBJECT_KEYWORD.lower() in subject.lower():

            for part in msg.walk():
                if part.get_content_disposition() and "attachment" in part.get_content_disposition():
                    filename = decode_mime_words(part.get_filename())

                    os.makedirs(f"attachments/{SENDER_EMAIL}", exist_ok=True)
                    filepath = os.path.join(f"attachments/{SENDER_EMAIL}", filename)

                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))

    mail.logout()
