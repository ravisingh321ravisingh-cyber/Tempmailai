import os
import telebot
import requests
import time
import threading

# Token hum Koyeb ki settings mein daalenge (Safe Method)
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ Bot Live Hai!\nNaya email chahiye toh /generate likho.")

@bot.message_handler(commands=['generate'])
def generate_email(message):
    chat_id = message.chat.id
    try:
        # Testing ke liye 1secmail API
        res = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()
        email = res[0]
        user, domain = email.split('@')
        bot.send_message(chat_id, f"📧 Aapka Temp Email:\n`{email}`\n\nMain OTP check kar raha hoon (2 mins)...", parse_mode="Markdown")

        def check_mail():
            # 150 seconds tak check karega
            for _ in range(15): 
                time.sleep(10)
                url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={user}&domain={domain}"
                msgs = requests.get(url).json()
                if msgs:
                    m_id = msgs[0]['id']
                    c = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={user}&domain={domain}&id={m_id}").json()
                    bot.send_message(chat_id, f"📩 **Naya Mail Aaya!**\n\nSubject: {c['subject']}\n\n{c['textBody']}")
                    break
        threading.Thread(target=check_mail).start()
    except Exception as e:
        bot.send_message(chat_id, "Kuch gadbad ho gayi, fir se try karein.")

bot.polling()
