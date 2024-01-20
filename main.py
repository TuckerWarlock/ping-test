import os
import time
import subprocess
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from emails import to_recipients, cc_recipients, bcc_recipients


# Load environment variables from .env
load_dotenv()
# Access environment variables
email_address = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_PASSWORD')
smtp_server = os.getenv('SMTP_SERVER')


def get_external_ip():
    response = requests.get('https://ifconfig.co/ip')
    return response.text.strip()
external_ip = get_external_ip()
print(f'Your external IP address is: {external_ip}')


def send_email(subject, body, to_emails, cc_emails=None, bcc_emails=None):
    # Set up your email details
    sender_email = email_address
    password = email_password

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ', '.join(to_emails)

    if cc_emails:
        message['Cc'] = ', '.join(cc_emails)

    if bcc_emails:
        message['Bcc'] = ', '.join(bcc_emails)

    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, 587) as server:
        server.starttls()
        server.login(sender_email, password)
        all_recipients = to_emails + (cc_emails or []) + (bcc_emails or [])
        server.sendmail(sender_email, all_recipients, message.as_string())


def send_outage_email(start_time, end_time):
    # Log the details and send an email to ISP support
    subject = 'Internet Outage Details'
    body = f'Outage start time: {start_time}\nOutage end time: {end_time}\nIP Address: {external_ip}'
    send_email(subject, body, to_recipients, cc_recipients, bcc_recipients)


def check_network_status():
    # result = subprocess.run(['ping', '-c', '4', modem_ip], stdout=subprocess.PIPE)
    result = subprocess.run(['ping', '-n', '4', external_ip], stdout=subprocess.PIPE)
    return result.returncode == 0


def main():
    online = True
    offline = not online

    while True:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        if not check_network_status():
            # Log the outage details
            if not online:
                print(f'Internet outage at {current_time}')
                online = False

            # Wait for a minute before checking again
            time.sleep(5)
        else:
            if offline:
                # Internet is back online
                outage_end_time = time.strftime('%Y-%m-%d %H:%M:%S')
                print(f'Internet online at {outage_end_time}')

                # Log the details and send an email to ISP support
                send_outage_email(current_time, outage_end_time)

                # Reset the flag when coming back online
                offline = False

            # Wait for a minute before checking again
            time.sleep(5)


if __name__ == "__main__":
    main()
