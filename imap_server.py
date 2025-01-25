import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re, os, email
from dotenv import load_dotenv
load_dotenv()
from URL_Analyzer import emailAnalyzer


def retrieve_email(user_email):
    IMAP_HOST = 'imap.gmail.com'
    IMAP_PORT = 993
    EMAIL = 'inboxinspector1@gmail.com'
    PASSWORD = os.getenv('EMAIL_PASSWORD')

    if not PASSWORD:
        raise ValueError("EMAIL_PASSWORD environment variable is not set.")

    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
        mail.login(EMAIL, PASSWORD)
        mail.select('inbox')

        original_sender = None
        urls = []
        email_body = None

        status, data = mail.search(None, f'(UNSEEN FROM "{user_email}")')
        if status == 'OK' and data[0]:
            for num in reversed(data[0].split()):
                status, data = mail.fetch(num, '(RFC822)')
                if status != 'OK':
                    print(f"Error fetching email: {status}")
                    continue

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

                if not email_body:
                    print(f"Email body is empty or could not be decoded.")
                    continue

                match = re.search(r'From:.*?<(?P<original_sender>[\w\.-]+@[\w\.-]+)>', email_body, re.DOTALL)
                if match:
                    original_sender = match.group('original_sender')
                urls.extend(re.findall(r'https?://\S+', email_body))
                mail.store(num, '-FLAGS', '\\Seen')
                break
        else:
            print(f"No unread emails from {user_email}.")
            return

        #Analyzing mail
        report = emailAnalyzer.email_report(original_sender, urls, email_body)
        send_report(user_email, report)

    except Exception as e:
        print(f"Error retrieving email for {user_email}: {e}")
    finally:
        try:
            mail.close()
            mail.logout()
        except Exception as e:
            print(f"Error closing mail connection: {e}")


def send_report(user_email, report):
    """Send analysis report to the user."""
    try:
        EMAIL = 'inboxinspector1@gmail.com'
        PASSWORD = os.getenv('EMAIL_PASSWORD')

        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = user_email
        msg['Subject'] = 'Inbox Inspector: Your Report is Ready!'

        # Prepare report content
        body = f"""\nDear User,

Thank you for using Inbox Inspector!

Inbox Inspector analyzes your emails for threats, such as phishing attempts and malicious content. 
Here is the analysis report:

- Email Address Score: {round(report["email_score"],2)}
- Email Body Score: {round(report["body_score"],2)}
"""
        if report["url_score"] != 0:
            body += f"- URL Score: {round(report['url_score'],2)}\n"

        final_score = 0.5 * report["body_score"] + 0.3 * report["email_score"] + 0.2 * report["url_score"]
        body += f"\nYour email has been classified as: "
        if final_score >= 0.8:
            body += "MALICIOUS EMAIL\n\nPlease avoid interacting with this email and report it."
        elif final_score >= 0.5:
            body += "PHISHING EMAIL\n\nAvoid clicking on any links and report it."
        else:
            body += "BENIGN EMAIL\n\nThis email appears safe."

        body += """\n\nThank you for your attention.\n\n- Inbox Inspector Team"""

        msg.attach(MIMEText(body, 'plain'))

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, user_email, msg.as_string())
        server.quit()

        print(f"Report sent successfully to {user_email}.")

    except Exception as e:
        print(f"Error sending report to {user_email}: {e}")
