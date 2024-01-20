# ping-test

## Overview

`ping-test` is a Python script that monitors the network connection and reports outages by sending emails with outage details. It checks for network outages, logs the start and end times of the outages, and notifies specified recipients via email.

## Features

- Monitors network connection and detects outages.
- Logs outage start and end times.
- Sends outage details via email to specified recipients.

## Prerequisites

Before running the script, ensure you have:

- Python installed on your system.
- Required Python packages installed. You can install them using `pip install -r requirements.txt`.
- A valid `.env` file with necessary environment variables.

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ping-test.git
2. Navigate to the project directory:

   ```bash
    cd ping-test
3. Install dependencies:

    ```bash
    pip install -r requirements.txt
4. Set up the environment variables in a .env file:
    ```bash
    EMAIL_ADDRESS=your_email@gmail.com
    EMAIL_PASSWORD=your_email_password
    SMTP_SERVER=your_smtp_server
5. Update the emails.py file with your recipient lists:

    ```bash
    # emails.py
    to_recipients = ['recipient1@example.com', 'recipient2@example.com']
    cc_recipients = ['cc1@example.com', 'cc2@example.com']
    bcc_recipients = ['bcc1@example.com', 'bcc2@example.com']
6. Run the script:

    ```bash
    python ping_test.py

## Configuration
- **EMAIL_ADDRESS**: Your email address for sending notifications.
- **EMAIL_PASSWORD**: Your email password or an App Password for secure authentication.
- **SMTP_SERVER**: Your SMTP server for sending emails.

## Customization
- You can customize the script further by modifying the `ping_test.py` file.
- Adjust the sleep duration in the main function based on how frequently you want to check the network status.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
