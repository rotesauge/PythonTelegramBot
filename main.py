import telebot
from convertor import ConvertException, Convertor
import traceback

bot = telebot.TeleBot('5928880745:AAHfI84JMoG4-9U4kPseTTGWdmbIvJwgDLM')

@bot.message_handler(commands=['start','help'])
def begin(message: telebot.types.Message):
        greet = f"Добро пожаловать, {message.chat.username}\n"
        text = greet + 'Для начала работы введите команду в формате:'\
                       '\n исходная валюта   валюта конвертации  количество'\
                       '\n Например: USD eur 10 '\
                       '\n для просмотра списка валют введите команду /valutes'
        bot.send_message(message.chat.id,text)

@bot.message_handler(commands=['valutes'])
def begin(message: telebot.types.Message):
        bot.reply_to(message, Convertor.get_all_valutes())


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise ConvertException('Неверное количество параметров!')
        cur1, cur2, amount = values
        answer = Convertor.get_price(cur1.upper(), cur2.upper(), amount)
    except ConvertException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)

@bot.message_handler(content_types=['photo','document'])
def say_lmao(message: telebot.types.Message):
        bot.reply_to(message, 'Неверный тип данных!')


bot.polling(none_stop=True)
