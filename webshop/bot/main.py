from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from .config import TOKEN
from ..db.models import Text, Category, Product
from .keyboards import START_KB
from .lookups import category_lookup, separator


bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    txt = Text.objects.get(title=Text.TITLES['greetings']).body

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(*[KeyboardButton(text=text) for text in START_KB.values()])

    bot.send_message(message.chat.id, txt, reply_markup=kb)


# @bot.message_handler(content_types=['text'])
# def choice_button(message):
#     if message.text == 'Категории':
#         kb = InlineKeyboardMarkup()
#
#         buttons = [InlineKeyboardButton(k, callback_data=k) for k in Category.title]
#         kb.add(*buttons)
#         bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=kb)
# @bot.callback_query_handler(func=lambda call: True)
# def my_query(call):
#     bot.send_message(call.from_user.id, Product.objects.(get)call.data)


'{lookup}{separator}{id}'
@bot.message_handler(content_types=['text'],
                     func=lambda message: message.text == START_KB['category'])
def categories(message):
    kb = InlineKeyboardMarkup()
    roots = Category.get_root_categories()

    buttons = [InlineKeyboardButton(text=category.title,
                                    callback_data=f'{category_lookup}{separator}{category.id}')
               for category in roots]
    kb.add(*buttons)
    bot.send_message(message.chat.id, text='Выберите категорию', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == category_lookup)
def category_click(call):
    category_id = call.data.split(separator)[1]
    category = Category.objects.get(id=category_id)
    kb = InlineKeyboardMarkup()

    if category.is_parent:
        subcategories = category.subcategories
        buttons = [InlineKeyboardButton(text=category.title,
                                        callback_data=f'{category_lookup}{separator}{category.id}')
                   for category in subcategories]
        kb.add(*buttons)
        bot.edit_message_text(category.title, chat_id=call.message.chat.id,
                              message_id=call.message.message_id, reply_markup=kb)

    else:
        print(f'Выводим продукты из категории {category.title}')


def start_bot():
    bot.polling()
