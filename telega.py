import telebot
from save_chart import save_chart
from telebot import types




bot = telebot.TeleBot('2052829317:AAEkM8WJKtZ9XJnoP8ymMyXDl1PSbe4e-Xg')


def telebot_listening():
    @bot.message_handler(commands=['start'])
    def start_command(message):
        bot.send_message(message.chat.id, f"Comands:\nall\nday\nhour")

    @bot.message_handler(commands=['all'])
    def day_command(message):
        # bot.send_message(message.chat.id, f"hour")
        save_chart('all')
        with open('test.png', 'rb') as img:
            bot.send_photo(message.chat.id, img)

    @bot.message_handler(commands=['day'])
    def day_command(message):
        # bot.send_message(message.chat.id, f"day")
        save_chart('day')
        with open('test.png', 'rb') as img:
            bot.send_photo(message.chat.id, img)

    @bot.message_handler(commands=['hour'])
    def day_command(message):
        # bot.send_message(message.chat.id, f"hour")
        save_chart('hour')
        with open('test.png', 'rb') as img:
            bot.send_photo(message.chat.id, img)
    bot.polling()



def send_mess(chat_id, text):
    bot.send_message(chat_id, text)

if __name__ == '__main__':
    telebot_listening()