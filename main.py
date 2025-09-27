# add these near top of file
import csv
from datetime import datetime

ADMIN_CHAT_ID = 7296485222  # tumhara real Telegram ID (as int)

# simple in-memory store for pending orders (restart will clear it)
pending_orders = {}  # key: user_id, value: {'amount': '50 UC', 'time': ..., 'tx': None}

# update UC selection handler to store choice and ask for payment proof
@bot.message_handler(func=lambda message: message.text in ['50 UC','100 UC','200 UC'])
def uc_order(message):
    user_id = message.from_user.id
    amount = message.text
    pending_orders[user_id] = {
        'amount': amount,
        'time': datetime.utcnow().isoformat(),
        'tx': None
    }

    bot.send_message(user_id, f"Selected {amount} ✅\nMinimum deposit: 500 PKR (UPASIA NUMBER 03303097845).\n"
                              "Account Name Rabia Hoga Payment karne ke baad TX/ID bhej do (type it here) and then type /confirm to notify me.")
    # optionally send a reply keyboard with Confirm button
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    markup.add('/confirm')
    bot.send_message(user_id, "When done, press /confirm", reply_markup=markup)

# handler to receive plain text (assume TX id or any text as payment proof) before /confirm
@bot.message_handler(func=lambda message: message.from_user.id in pending_orders and message.text and not message.text.startswith('/'))
def receive_payment_text(message):
    user_id = message.from_user.id
    text = message.text.strip()
    # store this as tx/proof
    pending_orders[user_id]['tx'] = text
    bot.send_message(user_id, "Payment info saved. Now type /confirm to notify the admin.")

# improved confirm handler: forwards full info to admin and logs CSV
@bot.message_handler(commands=['confirm'])
def confirm(message):
    user = message.from_user
    user_id = user.id

    if user_id not in pending_orders:
        bot.send_message(user_id, "Koi pending order nahi mila. Pehle UC select karo.")
        return

    order = pending_orders[user_id]
    amount = order.get('amount', 'Unknown')
    tx = order.get('tx', 'No payment info provided')
    time_iso = order.get('time', datetime.utcnow().isoformat())

    # notify user
    bot.send_message(user_id, "Request received! Main admin ko bhej raha hoon, verification ke baad main aapko UC bhej dunga. 💳")

    # prepare admin message
    username = f"@{user.username}" if user.username else user.first_name
    admin_msg = (
        f"📥 New UC Request\n"
        f"User: {username}\n"
        f"User ID: {user_id}\n"
        f"Amount: {amount}\n"
        f"Payment/Tx: {tx}\n"
        f"Requested at (UTC): {time_iso}\n"
    )

    # send to admin
    bot.send_message(ADMIN_CHAT_ID, admin_msg)

    # log to CSV
    try:
        with open('orders.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.utcnow().isoformat(), user_id, username, amount, tx])
    except Exception as e:
        # if logging fails, at least notify admin
        bot.send_message(ADMIN_CHAT_ID, f"⚠️ Error logging order: {e}")

    # clear pending order for user (or keep it if you want)
    pending_orders.pop(user_id, None)
