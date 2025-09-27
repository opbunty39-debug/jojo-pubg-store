import telebot
from telebot import types

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_photo(chat_id, open('pubg_banner.jpg', 'rb'), caption="Welcome to JoJo PUBG Shop! 💥\nSelect your UC:")
    
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add('50 UC', '100 UC', '200 UC')
    bot.send_message(chat_id, "Choose UC amount:", reply_markup=markup)

# UC Selection
@bot.message_handler(func=lambda message: message.text in ['50 UC','100 UC','200 UC'])
def uc_order(message):
    chat_id = message.chat.id
    amount = message.text
    bot.send_message(chat_id, f"Selected {amount} ✅\nSend payment via USDT (UpAsia). Minimum 500 PKR.")
    bot.send_message(chat_id, "After payment, type /confirm to notify me.")

# Confirm Payment
@bot.message_handler(commands=['confirm'])
def confirm(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Request received! I will verify your payment and send UC shortly. 💳")

bot.infinity_polling()
