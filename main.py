ADMIN_CHAT_ID = 7296485222 # apna Telegram ID yahan daal

@bot.message_handler(commands=['confirm'])
def confirm(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Request received! I will verify your payment and send UC shortly. 💳")
    bot.send_message(ADMIN_CHAT_ID, f"User @{message.from_user.username} requested {message.text}")
