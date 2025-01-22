import os
import smtplib
from smtplib import SMTPAuthenticationError
import sys
import time
import random
import socket
import uuid
import platform
from config import senders_info


def clear_screen():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # macOS/Linux
        os.system('clear')
        sys.stdout.write("\033[8;27;85t")  # Resize terminal to 27 rows x 85 columns


clear_screen()

ART = """  __  __       _ _   ____                  _               
 |  \/  |     (_) | |  _ \                | |              
 | \  / | __ _ _| | | |_) | ___  _ __ ___ | |__   ___ _ __ 
 | |\/| |/ _` | | | |  _ < / _ \| '_ ` _ \| '_ \ / _ \ '__|
 | |  | | (_| | | | | |_) | (_) | | | | | | |_) |  __/ |   
 |_|  |_|\__,_|_|_| |____/ \___/|_| |_| |_|_.__/ \___|_|   
                                                           
                                                           """


def print_ascii_art(art):
    RED = '\033[91m'
    END = '\033[0m'

    terminal_size = os.get_terminal_size()
    terminal_width = terminal_size.columns
    art_lines = art.splitlines()

    centered_art = "\n".join(
        line.ljust(terminal_width) for line in art_lines
    )
    print(f"{RED}{centered_art}{END}")


BLUE = '\033[94m'
RED = '\033[91m'
WHITE = '\033[97m'
END = '\033[0m'


def get_non_negative_integer(prompt):
    while True:
        try:
            print(f"{BLUE}{prompt}{END}", end='')
            value = input()
            print(f"{RED}{value}{END}\n")  # Echo back the input in red
            integer_value = int(value)
            if integer_value < 0:
                raise ValueError("The number cannot be negative.")
            return integer_value
        except ValueError as e:
            print(f"{RED}Invalid input. Please enter a non-negative integer.\n{END}", str(e))


def get_non_empty_input(prompt, error_message="Input cannot be empty. Please try again."):
    while True:
        print(f"{BLUE}{prompt}{END}", end='')
        value = input().strip()
        if not value:
            print(f"{RED}{error_message}{END}\n")
        else:
            print(f"{RED}{value}{END}\n")  # Echo back the input in red
            return value


def get_system_info():
    user_ip = socket.gethostbyname(socket.gethostname())
    user_mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff)
                         for i in range(0, 8 * 6, 8)][::-1])
    user_os = platform.system()
    return user_ip, user_mac, user_os


def show_menu():
    print_ascii_art(ART)
    print(f"{BLUE}Select which Email the recipient uses:{END}")
    print(f"{RED}[1] Gmail")
    print(f"[2] Outlook")
    print(f"[3] Other")
    print(f"[4] IP - Check{END}")


def select_email_service():
    while True:
        clear_screen()
        show_menu()
        choice = input(f"{BLUE}Mail Server: {END}").strip()
        if choice in ['1', '2', '3', '4']:
            print(f"{RED}{choice}{END}\n")  # Optionally echo back the choice in red
        if choice == '1':
            return 'gmail'
        elif choice == '2' or choice == '3':
            return 'outlook'
        elif choice == '4':
            user_ip, user_mac, user_os = get_system_info()
            print(f"{WHITE}IP: {user_ip}\nMAC: {user_mac}\nOS: {user_os}{END}")
            print(f"{WHITE}This Information can be Exposed After Sending the mails. Make sure to use a VPN. The best Option is a TOR connection.{END}\n")
            input(f"{BLUE}Press Enter to return to the menu...{END}")
        else:
            print(f"{RED}Invalid selection. Please enter 1, 2, 3, or 4.{END}\n")


email_service = select_email_service()

if email_service == 'gmail':
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
else: 
    smtp_server = 'smtp.office365.com'
    smtp_port = 587

sender_email, sender_password = random.choice(senders_info[email_service])

recipient_email = get_non_empty_input("Please enter the recipient's email address: ")
recipient_name = get_non_empty_input("What is the recipient's name?: ")
sender_alias = get_non_empty_input("Enter the display name for the sender (IMPORTANT: DO NOT USE YOUR REAL NAME!): ")
number_of_emails_per_account = get_non_negative_integer("How many emails would you like to send per account?: ")
delay = get_non_negative_integer("Enter the delay (in seconds) between sending emails: ")

message_body = get_non_empty_input("Enter the content of your email message: ")

for sender_email, sender_password in senders_info[email_service]:
    email_counter = 1
    print(f"{RED}Sending from {sender_email}\n{END}")
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            try:
                server.login(sender_email, sender_password)
                print(f"{RED}Login successful. Preparing to send emails...\n{END}")
                input(f"{WHITE}Emails Ready, Press enter to deploy {END}")
            except SMTPAuthenticationError:
                print(f"{RED}Failed to send email from {sender_email}. The username or password might be incorrect. Make sure to add an app password, not your real one{END}\n")
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
                print(f"{RED}Email {email_counter} from {sender_email} to {recipient_email} has been sent.\n{END}")
                time.sleep(delay)
                email_counter += 1

    except Exception as e:
        print(f"An error occurred: {e}\n")
        
    if len(senders_info[email_service]) > 1:
        print("Preparing next sender...\n")

print(f"{RED}Process completed.\n{END}")
