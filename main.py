import os
import smtplib
from smtplib import SMTPAuthenticationError
import sys
import time
import random


senders_info = {
    'gmail': [
        ('example@gmail.com', 'password123'),
        ('example@gmail.com', 'password123'),
    ],
    'outlook': [
        ('example@outlook.com', 'password1'),
    ],
}


BLUE = '\033[94m'
GREEN = '\033[32m'
RED = '\033[91m'
WHITE = '\033[97m'
CYAN = '\033[36m'
ORANGE = '\033[93m'
END = '\033[0m'

def clear_screen():
    os.system('clear')

def loading_screen():
    clear_screen()
    print(f"{BLUE}Loading ...{END}")
    time.sleep(2)
    for service, accounts in senders_info.items():
        for email, password in accounts:
            if "example@" in email:
                print(f"{RED}[-]{END}{CYAN}sender_info is not Configured, tool won't work{END}")
                time.sleep(1)
                print(f"{RED}[-]{END}{CYAN}Make sure the e-mail and AppPassword is correct{END}")
                time.sleep(4)
                print(f"{BLUE}Don’t forget to star our tool ⭐️{END}")
                time.sleep(2)
                print("https://github.com/VOYXXY/EB-Spammer/tree/main")
                time.sleep(4)
                return
    time.sleep(1)
    print(f"{BLUE}Don’t forget to star our tool ⭐️{END}")
    time.sleep(1)
    print("https://github.com/VOYXXY/EB-Spammer/tree/main")
    time.sleep(1)
    print(f"{GREEN}[+]{END}{CYAN}Tool ready to use ...[ ✔ ]{END}")
    time.sleep(3)

ART = """ 
________  _______
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
            print(f"{RED}[-]{END}{CYAN}Invalid input. Please enter a number.{END}")

def get_non_empty_input(prompt):
    while True:
        print(f"{BLUE}{prompt}{END}", end='')
        value = input().strip()
        if value:
            return value

def show_menu():
    print_ascii_art(ART)
    print()
    print(f"{ORANGE}[!] Select a Template :{END}")
    print()
    print(f"{GREEN}[1]{END}{CYAN}Gmail")
    print(f"{GREEN}[2]{END}{CYAN}Outlook")
    print(f"{GREEN}[3]{END}{CYAN}Other")
    print(f"{GREEN}[4]{END}{CYAN}OTP-OpenAI")
    print()

def select_email_service():
    while True:
        clear_screen()
        show_menu()
        choice = input(f"{GREEN}[>]{END}{CYAN}Mail Service : ").strip()
        if choice == '1':
            return 'gmail'
        elif choice == '2' or choice == '3':
            return 'outlook'
        elif choice == '4':
            return 'otp'
        else:
            print(f"{RED}[-]{END}{CYAN}Invalid input. Please enter a number.{END}")

def check_temporary_email(email):
    if email.endswith('@msssg.com') or email.endswith('@bcooq.com'):
        print(f"{ORANGE}[!]This mail is possibly owned by a 10-minute mail service. Do you wish to continue anyways? (y/n){END}")
        while True:
            choice = input().lower()
            if choice == 'y':
                return True
            elif choice == 'n':
                print(f"{RED}Process aborted by user.{END}")
                sys.exit()
            else:
                print(f"{ORANGE}[!]Invalid input. Please enter 'y' or 'n'.{END}")

def generate_otp():
    return random.randint(100000, 999999)

loading_screen()
email_service = select_email_service()

if email_service == 'gmail':
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
elif email_service == 'outlook':
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
elif email_service == 'otp':
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

print()
recipient_email = get_non_empty_input(
    f"{GREEN}[+]{END}{CYAN} Recipient's email: {END}"
)
check_temporary_email(recipient_email)

if email_service == 'otp':
    print()
    number_of_emails_per_account = get_non_negative_integer(
        f"{GREEN}[+]{END}{CYAN} Number of OTP emails to send: {END}"
    )
    delay = get_non_negative_integer(
        f"{GREEN}[+]{END}{CYAN} Delay (in seconds) between emails: {END}"
    )
    Link_openAI = get_non_empty_input(
        f"{GREEN}[+]{END}{CYAN} Link (OpenAI): {END}"
    )
    Link_HelpCenter = get_non_empty_input(
        f"{GREEN}[+]{END}{CYAN} Link (HelpCenter): {END}"
    )

    for sender_email, sender_password in senders_info['gmail']:
        email_counter = 1
        print(f"{GREEN}[+]{END}{CYAN} Sending from {sender_email}{END}")
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                try:
                    server.login(sender_email, sender_password)
                    print()
                    print(f"{GREEN}[+]{END}{CYAN} Login successful..[ ✔ ]{END}")
                except SMTPAuthenticationError:
                    print(f"{RED}[-]{END}{CYAN} Login failed for {sender_email}.{END}")
                    continue

                for _ in range(number_of_emails_per_account):
                    otp_code = generate_otp()
                    customized_message = f"""From: ChatGTP<{sender_email}>
To: {recipient_email}
Subject: Your Code for ChatGPT: {otp_code}

Your code for ChatGPT: {otp_code}

Please enter this temporary verification code to continue:

{otp_code}

If you did not attempt to create a ChatGPT account, please ignore this email.

Best regards,
The ChatGPT Team

ChatGPT {Link_openAI}

Help Center {Link_HelpCenter}
"""
                    server.sendmail(sender_email, recipient_email, customized_message.encode('utf-8'))
                    print(f"{GREEN}[+]{END}{CYAN}OTP Email {email_counter} sent to {recipient_email}.{END}")
                    time.sleep(delay)
                    email_counter += 1

        except Exception as e:
            print(f"Error: {e}")

else:
    recipient_name = get_non_empty_input(
        f"{GREEN}[+]{END}{CYAN} Recipient's name: {END}"
    )
    sender_alias = get_non_empty_input(
        f"{GREEN}[+]{END}{CYAN} Sender alias: {END}"
    )
    number_of_emails_per_account = get_non_negative_integer(
        f"{GREEN}[+]{END}{CYAN} Number of emails per account: {END}"
    )
    delay = get_non_negative_integer(
        f"{GREEN}[+]{END}{CYAN} Delay (in seconds) between emails: {END}"
    )
    message_body = get_non_empty_input(
        f"{GREEN}[+]{END}{CYAN} Email message content: {END}"
    )
    subject_line = get_non_empty_input(
        f"{GREEN}[+]{END}{CYAN} Enter subject line: {END}"
    )

    for sender_email, sender_password in senders_info[email_service]:
        email_counter = 1
        print(f"{GREEN}[+]{END}{CYAN} Sending from {sender_email}{END}")
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                try:
                    server.login(sender_email, sender_password)
                    print()
                    print(f"{GREEN}[+]{END}{CYAN} Login successful..[ ✔ ]{END}")
                except SMTPAuthenticationError:
                    print(f"{RED}[-]{END}{CYAN} Login failed for {sender_email}.{END}")
                    continue

                for _ in range(number_of_emails_per_account):
                    customized_message = f"""From: {sender_alias}<{sender_email}>
To: {recipient_email}
Subject: {subject_line}

Hello {recipient_name}!

{message_body}

Warm regards,
{sender_alias}
"""
                    server.sendmail(sender_email, recipient_email, customized_message.encode('utf-8'))
                    print(f"{GREEN}[+]{END}{CYAN}Email {email_counter} sent to {recipient_email}.{END}")
                    time.sleep(delay)
                    email_counter += 1

        except Exception as e:
            print(f"Error: {e}")

print(f"{ORANGE}[!] Process completed.{END}")
