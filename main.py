import telebot
from config import current, TOKEN
from extensions import Message

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def comand_start(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Для конвертациии валюты вам необходимо ввести:\n<имя ковертируемой валюты>\n<имя валюты в которую хотите сконвертировать>\n<количество конвертируемой валюты>')
    bot.send_message(message.chat.id, 'Для получения списка конвертируемых валют введите команду: /list')

@bot.message_handler(commands=['list'])
def comand_start(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in current:
        text += '\n'
        text += key
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def answer_text(message: telebot.types.Message):
    c = Message(message.text)
    if c.test():
        try:
            bot.send_message(message.chat.id, f'Результат конвертации: {c.amount} {current[c.f]} = {Message.get_price(c.to, c.f, c.amount)} {current[c.to]}')
        except Exception:
            bot.send_message(message.chat.id, 'К сожалению, что-то пошло не так, пожалуйста, повторите попытку еще раз.')
    else:
        bot.reply_to(message, c.exception)

bot.polling(none_stop=True)