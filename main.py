import os
import smtplib
import platform
from smtplib import SMTPAuthenticationError
import sys
import requests
import time
import threading
import random
from config import senders_info, discord_token
import logging
from datetime import datetime

GITHUB_REPO = "VOYXXY/EB-Spammer"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
LOCAL_VERSION_FILE = "local_version.txt"

BLUE = '\033[94m'
GREEN = '\033[32m'
RED = '\033[91m'
WHITE = '\033[97m'
CYAN = '\033[36m'
ORANGE = '\033[93m'
END = '\033[0m'

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear') 

def get_latest_github_version():
    try:
        response = requests.get(GITHUB_API_URL, timeout=5)
        if response.status_code == 200:
            return response.json().get("tag_name", "Unknown")
    except requests.RequestException as e:
        print(f"{RED}[-] Error Getting latest github version : {e}{END}")
    return None

def get_local_version():
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()
    return "Unknown"

def check_for_updates():
    print(f"{CYAN}[~] Checking for updates...{END}")
    latest_version = get_latest_github_version()
    local_version = get_local_version()
    
    if latest_version and latest_version != local_version:
        print(f"{GREEN}[+] Update Available , Version : {latest_version}{END}")
        with open(LOCAL_VERSION_FILE, "w") as f:
            f.write(latest_version)
    else:
        print(f"{BLUE}[✔] You have the newest version  ({local_version}){END}")

def loading_screen():
    clear_screen()
    print(f"{BLUE}Loading ...{END}")
    time.sleep(1)
    for service, accounts in senders_info.items():
        for email, password in accounts:
            if "example@" in email:
                print(f"{RED}[-]{END}{CYAN}sender_info is not Configured, tool won't work{END}")
                time.sleep(1)
                print(f"{RED}[-]{END}{CYAN}Make sure the e-mail and AppPassword is correct{END}")
                time.sleep(1)
                print(f"{BLUE}Don’t forget to star our tool ⭐️{END}")
                time.sleep(2)
                check_for_updates()
                return
    time.sleep(1)
    print(f"{BLUE}Don’t forget to star our tool ⭐️{END}")
    time.sleep(1)
    print(f"{GREEN}[+]{END}{CYAN}Tool ready to use ...[ ✔ ]{END}")
    check_for_updates()
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

def MassDM(token, chunk, message, num_messages, delay, target_user):
    for channel in channels:
        for user in [x["username"]+"#"+x["discriminator"] for x in channel["recipients"]]:
            try:
                print(f"Messaging {user}")
                for _ in range(num_messages):
                    requests.post(f"https://discord.com/api/v9/channels/{channel['id']}/messages", 
                                  headers={'Authorization': token}, 
                                  data={"content": f"{message}"})
                    print(f"[+] Messaged: {user}")
                    time.sleep(delay)
            except Exception as e:
                print(f"[-] Error: {e}")

def show_menu():
    print_ascii_art(ART)
    print()
    print(f"{ORANGE}[!] Select a Template :{END}")
    print()
    print(f"{GREEN}[1]{END}{CYAN}Gmail")                    
    print(f"{GREEN}[2]{END}{CYAN}Outlook")
    print(f"{GREEN}[3]{END}{CYAN}Other")
    print(f"{GREEN}[4]{END}{CYAN}OTP")
    print(f"{GREEN}[5]{END}{CYAN}Discord-Webhook")
    print(f"{GREEN}[6]{END}{CYAN}Discord-DM")
    print()

def select_email_service():
    while True:
        clear_screen()
        show_menu()
        choice = input(f"{GREEN}[>]{END}{CYAN} Mail Service : ").strip()
        if choice == '1':
            return 'gmail'
        elif choice == '2' or choice == '3':
            return 'outlook'
        elif choice == '4':
            return 'otp'
        elif choice == '5':
            return 'dc'
        elif choice == '6':
            return 'dcDM'
        else:
            print(f"{RED}[-]{END}{CYAN} Invalid input. Please enter a number.{END}")

def check_temporary_email(email):
    if email.endswith('@msssg.com') or email.endswith('@bcooq.com'):
        print(f"{ORANGE}[!] This mail is possibly owned by a 10-minute mail service. Do you wish to continue anyways? (y/n){END}")
        while True:
            choice = input().lower()
            if choice == 'y':
                return True
            elif choice == 'n':
                print(f"{RED}Process aborted by user.{END}")
                sys.exit()
            else:
                print(f"{ORANGE}[!] Invalid input. Please enter 'y' or 'n'.{END}")

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
else:
    print(f"[-] Invalid choice: {email_service}")  
    exit(0)

print()
if email_service == 'dc':
    print()
    webhook_url = get_non_empty_input(
        f"{GREEN}[+]{END}{CYAN} Webhook URL: {END}"
    )
    number_of_messages = get_non_negative_integer(
        f"{GREEN}[+]{END}{CYAN} Number of Messages to send: {END}"
    )
    delay = get_non_negative_integer(
        f"{GREEN}[+]{END}{CYAN} Delay (in seconds) between Messages: {END}"
    )
    message = get_non_empty_input(
        f"{GREEN}[+]{END}{CYAN} Message : {END}"
    )
    webhook_name = get_non_empty_input(
        f"{GREEN}[+]{END}{CYAN} Webhook Name  : {END}"
    )
    random_name_per_message = get_non_empty_input(
        f"{GREEN}[+]{END}{CYAN} Random name per message (y/n): {END}"
    ).lower() == 'y'

    random_names = []
    if random_name_per_message:
        try:
            with open("src/random_name.txt", "r") as file:
                random_names = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print("random_name.txt not found in 'src' directory.")

    delete_webhook = get_non_empty_input(
        f"{GREEN}[+]{END}{CYAN} Do you want to delete the webhook after sending all messages? (y/n): {END}"
    ).lower() == 'y'

    for i in range(number_of_messages):
        name = random.choice(random_names) if random_name_per_message and random_names else webhook_name
        data = {
            "content": message,
            "username": name
        }
        
        try:
            response = requests.post(webhook_url, json=data)
            if response.status_code == 204:
                print(f"{GREEN}[+]{END}{CYAN}Message {i+1} sent to {webhook_url}.{END}")
            else:
                print(f"{RED}[-]{END}{CYAN} Failed to send message {i+1}. Status code: {response.status_code}{END}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

        time.sleep(delay)

    if delete_webhook:
        try:
            delete_response = requests.delete(webhook_url)
            if delete_response.status_code == 204:
                print(f"{GREEN}[+]{END}{CYAN}Webhook deleted after sending all messages.{END}")
            else:
                print(f"{RED}[-]{END}{CYAN} Failed to delete webhook. Status code: {delete_response.status_code}{END}")
        except requests.exceptions.RequestException as e:
            print(f"Error while deleting the webhook: {e}")

    print(f"{ORANGE}[!] Webhook process completed.{END}")
    exit(0)

if email_service == 'dcDM':
    print()
    token = discord_token['token'][0]
    num_messages = get_non_negative_integer(
        f"{GREEN}[+]{END}{CYAN} Number of Messages to send: {END}"
    )
    delay = get_non_negative_integer(
        f"{GREEN}[+]{END}{CYAN} Delay (in seconds) between Messages: {END}"
    )
    message = get_non_empty_input(
        f"{GREEN}[+]{END}{CYAN} Message: {END}"
    )
    target_user = get_non_empty_input(
        f"{GREEN}[+]{END}{CYAN} All friends or userID (all/ID): {END}"
    )

    validityTest = requests.get(
        'https://discordapp.com/api/v6/users/@me',
        headers={'Authorization': token, 'Content-Type': 'application/json'}
    )

    if validityTest.status_code != 200:
        print("[-] Invalid Discord Account token")
        input(f"{ORANGE}[!] Press Enter to exit...{END}")
        exit(0)

    channels = requests.get(
        "https://discord.com/api/v9/users/@me/channels",
        headers={'Authorization': token}
    ).json()

    if not channels:
        print("[-] No DM channels found.")
        input(f"{ORANGE}[!] Press Enter to exit...{END}")
        exit(0)

    if target_user.lower() != "all":
        channels = [channel for channel in channels if "recipients" in channel and any(user["id"] == target_user for user in channel["recipients"])]

        if not channels:
            print("[-] No matching DM channel found for the given userID.")
            input(f"{ORANGE}[!] Press Enter to exit...{END}")
            exit(0)

    for chunk in [channels[i:i+3] for i in range(0, len(channels), 3)]:
        MassDM(token, chunk, message, num_messages, delay, target_user)

    print("[+] DM spam completed.")
    exit(0)
#else:
#    print("[-] Invalid choice.")
  #  exit(0)

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
    company = get_non_empty_input(
        f"{GREEN}[+]{END}{CYAN} Company name: {END}"
    )
    Link_No = get_non_empty_input(
        f"{GREEN}[+]{END}{CYAN} Link : {END}"
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
Subject: Your Code for {company}: {otp_code}

Your code for {company}: {otp_code}

Please enter this temporary verification code to continue:

{otp_code}

If you did not attempt to create a {company} account, please ignore this email.

Best regards,
The {company} Team

{company} {Link_No}

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
