from webshop.bot.main import start_bot
from flask import Flask, request, abort
from telebot.types import Update

app = Flask(__name__)


@app.route('/tg', method=['POST'])
def webhook():
    if request.headers.get('contetnt-type') == 'application/json':
        json_string = request.data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_update([update])
    else:
        abort(403)
if __name__ == '__main__':
    
