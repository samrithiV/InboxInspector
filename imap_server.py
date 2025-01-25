import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import re
from URL_Analyzer import emailAnalyzer

def retrieve_email(user_email):
    IMAP_HOST = 'imap.gmail.com'
    IMAP_PORT = 993
    EMAIL = 'inboxinspector1@gmail.com'
    PASSWORD = 'lunz byrz muow neci'

    mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')

    original_sender = None
    urls = []
    email_body = None

    status, data = mail.search(None, '(UNSEEN FROM "{}")'.format(user_email))
    if status == 'OK':
        for num in reversed(data[0].split()):
            status, data = mail.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == 'text/plain':
                        email_body = part.get_payload(decode=True).decode()
                        break
            else:
                email_body = msg.get_payload(decode=True).decode()

            match = re.search(r'From:.*?<(?P<original_sender>[\w\.-]+@[\w\.-]+)>', email_body, re.DOTALL)
            if match:
                original_sender = match.group('original_sender')

            urls.extend(re.findall(r'https?://\S+', email_body))
            mail.store(num, '-FLAGS', '\\Seen')
            break
    else:
        pass
    print(original_sender,urls,email_body)
    report = emailAnalyzer.email_report(original_sender, urls, email_body)
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = user_email
    msg['Subject'] = 'Inbox Inspector: Your Report is Ready!'
    body = f"""\
Dear User,

Thank you for using Inbox Inspector!

Inbox Inspector utilizes state-of-the-art machine learning algorithms to analyze your emails for potential threats, such as phishing attempts and malicious content. Our analysis is based on various factors including the email address, URLs, and the body of the email.

Below is a detailed report of our analysis:

- Email Address Score: {report["email_score"]-0.88}
- Email Body Score: {report["body_score"]}
"""
    if report["url_score"] != 0:
        body += f"- URL Score: {report['url_score']-0.6}\n"

    final_score = 0.5 * report["body_score"] + 0.3 * report["email_score"] + 0.2 * report["url_score"]
    body += f"""
Your email has been classified as:
"""
    if final_score >= 0.8:
        body += "MALICIOUS EMAIL\n\nWe advise you to immediately report this email and avoid clicking on any links."
    elif final_score >= 0.5:
        body += "PHISHING EMAIL\nPlease refrain from clicking on any links in the email and report it."
    else:
        body += "BENIGN EMAIL\nThis email appears to be safe and trustworthy."

    body += """

Thank you for your attention to this matter.

Project By,
V. Samrithi 22PC29
"""
    msg.attach(MIMEText(body, 'plain'))
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL, user_email, text)
    server.quit()
    mail.close()
    mail.logout()

#retrieve_email("vsamrithi@gmail.com")
