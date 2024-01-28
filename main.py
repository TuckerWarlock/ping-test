import os
import time
import subprocess
import smtplib
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


# Instead of getting your IP address and potentially doxxing yourself, just ping Google's DNS
# def get_external_ip():
#     try:
#         response = requests.get('https://ifconfig.co/ip')
#         external_ip = response.text.strip()
#         if external_ip is not None:
#             print(f'Online with IP - {external_ip}')
#         return external_ip
#     except ConnectionError:
#         print(f'Unable to determine External IP - check connection')
#         return None


def check_network_status():
    try:
        result = subprocess.run(['ping', '-n', '4', '8.8.8.8'], stdout=subprocess.PIPE)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f'Error in check_network_status \n{e}')
        return False
    except TypeError:
        print(f'Error pinging Google DNS - check network connection')
        return False


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
    body = f'Outage start time: {start_time}\nOutage end time: {end_time}'
    send_email(subject, body, to_recipients, cc_recipients, bcc_recipients)


def main():
    outage_start_time = None
    outage = False

    while True:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        online = check_network_status()
        # Network is offline
        if not online:
            if outage == False:
                outage_start_time = current_time
                print(f'Internet outage started at {outage_start_time}')
            outage = True
            continue

        # Network is back online
        if online and outage:
            outage_end_time = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f'Internet back online at {outage_end_time}')
            outage = False
            # Log the details and send an email to ISP support
            send_outage_email(outage_start_time, outage_end_time)

        # Wait for a minute before checking again
        time.sleep(60)


if __name__ == "__main__":
    main()
