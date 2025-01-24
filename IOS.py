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
WHITE = '\033[97m'
ORANGE = '\033[93m'
END = '\033[0m'

def loading_screen():
    clear_screen()
    print(f"{BLUE}Loading ...{END}")
    time.sleep(2)  # Ladezeit simulieren
    # Überprüfung der Konfiguration
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

ART = """ ________  _______
/        |/       \ 
$$$$$$$$/ $$$$$$$  |
$$ |__    $$ |__$$ |
$$    |   $$    $$< 
$$$$$/    $$$$$$$  |
$$ |_____ $$ |__$$ |
$$       |$$    $$/ 
$$$$$$$$/ $$$$$$$/
"""

def print_ascii_art(art):
    RED = '\033[91m'
    END = '\033[0m'
    print(f"{RED}{art}{END}")

def get_non_negative_integer(prompt):
    while True:
        try:
            print(f"{BLUE}{prompt}{END}", end='')
            value = input()
            return int(value)
        except ValueError:
            print(f"{RED}Invalid input. Please enter a number.{END}")

def get_non_empty_input(prompt):
    while True:
        print(f"{BLUE}{prompt}{END}", end='')
        value = input().strip()
        if value:
            return value

def show_menu():
    print_ascii_art(ART)
    print(f"{BLUE}Select Email Service:{END}")
    print(f"{RED}[1] Gmail")
    print(f"[2] Outlook")
    print(f"[3] Other{END}")

def select_email_service():
    while True:
        clear_screen()
        show_menu()
        choice = input(f"{BLUE}Mail Server: {END}").strip()
        if choice == '1':
            return 'gmail'
        elif choice == '2' or choice == '3':
            return 'outlook'
        else:
            print(f"{RED}Invalid selection. Please enter 1, 2, or 3.{END}")

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

email_service = select_email_service()

if email_service == 'gmail':
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
else: 
    smtp_server = 'smtp.office365.com'
    smtp_port = 587

recipient_email = get_non_empty_input("Recipient's email: ")
check_temporary_email(recipient_email)  # Überprüfung auf temporäre E-Mails
recipient_name = get_non_empty_input("Recipient's name: ")
sender_alias = get_non_empty_input("Sender alias: ")
number_of_emails_per_account = get_non_negative_integer("Number of emails per account: ")
delay = get_non_negative_integer("Delay (in seconds) between emails: ")
message_body = get_non_empty_input("Email message content: ")

for sender_email, sender_password in senders_info[email_service]:
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
                continue

            for _ in range(number_of_emails_per_account):
                subject_line = f"Custom Email - {email_counter}"
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

print(f"{RED}Process completed.{END}")
