import os
import smtplib
from smtplib import SMTPAuthenticationError
import sys
import time

# Konfiguration der Absenderinformationen
senders_info = {
    'gmail': [
        ('example@gmail.com', 'password123'),
        ('example@gmail.com', 'password123'),
    ],
    'outlook': [
        ('example1@outlook.com', 'password1'),
    ],
}

def clear_screen():
    os.system('clear')

BLUE = '\033[94m'
RED = '\033[91m'
ORANGE = '\033[93m'
END = '\033[0m'

def loading_screen():
    clear_screen()
    print(f"{BLUE}Loading ...{END}")
    time.sleep(2)
    for service, accounts in senders_info.items():
        for email, password in accounts:
            if "example@" in email:
                print(f"{RED}Tool won’t work correctly, sender_info is not configured.{END}")
                time.sleep(1)
                print(f"{BLUE}Don’t forget to star our tool ⭐️{END}")
                time.sleep(2)
                return
    print(f"{BLUE}Tool ready to use!{END}")
    time.sleep(1)

def get_non_negative_integer(prompt):
    while True:
        try:
            print(f"{BLUE}{prompt}{END}", end='')
            return int(input())
        except ValueError:
            print(f"{RED}Invalid input. Please enter a number.{END}")

def get_non_empty_input(prompt):
    while True:
        print(f"{BLUE}{prompt}{END}", end='')
        value = input().strip()
        if value:
            return value

def check_temporary_email(email):
    if email.endswith('@msssg.com') or email.endswith('@bcooq.com'):
        print(f"{ORANGE}ATTENTION: This mail is possibly owned by a 10-minute mail service. Do you wish to continue anyways? (y/n){END}")
        while True:
            choice = input().lower()
            if choice == 'y':
                return True
            elif choice == 'n':
                print(f"{RED}Process aborted by user.{END}")
                sys.exit()
            else:
                print(f"{RED}Invalid input. Please enter 'y' or 'n'.{END}")

# Ladebildschirm und Konfigurationsprüfung
loading_screen()

email_service = get_non_empty_input("Select Email Service [gmail/outlook]: ").lower()
smtp_server, smtp_port = ('smtp.gmail.com', 587) if email_service == 'gmail' else ('smtp.office365.com', 587)

recipient_email = get_non_empty_input("Recipient's email: ")
check_temporary_email(recipient_email)
recipient_name = get_non_empty_input("Recipient's name: ")
sender_alias = get_non_empty_input("Sender alias: ")
number_of_emails_per_account = get_non_negative_integer("Number of emails per account: ")
delay = get_non_negative_integer("Delay (in seconds) between emails: ")
message_body = get_non_empty_input("Email message content: ")
subject_line = get_non_empty_input("Subject line: ")

# Senden von E-Mails
all_emails_sent = True
for sender_email, sender_password in senders_info.get(email_service, []):
    email_counter = 1
    print(f"{RED}Sending from {sender_email}{END}")
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            try:
                server.login(sender_email, sender_password)
                print(f"{RED}Login successful.{END}")
            except SMTPAuthenticationError:
                print(f"{RED}Login failed for {sender_email}.{END}")
                all_emails_sent = False
                continue

            for _ in range(number_of_emails_per_account):
                customized_message = f"""From: {sender_email}
To: {recipient_email}
Subject: {subject_line}

Hello {recipient_name}!

{message_body}

Warm regards,
{sender_alias}
"""
                server.sendmail(sender_email, recipient_email, customized_message.encode('utf-8'))
                print(f"{RED}Email {email_counter} sent to {recipient_email}.{END}")
                time.sleep(delay)
                email_counter += 1

    except Exception as e:
        print(f"Error: {e}")
        all_emails_sent = False

if all_emails_sent:
    print(f"{BLUE}All emails sent successfully! Don’t forget to star our tool ⭐️{END}")
else:
    print(f"{RED}Some emails could not be sent. Please check the logs.{END}")

print(f"{RED}Process completed.{END}")
