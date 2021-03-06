import re
import os
from flask import Flask, request
import telebot
import lathings
import numpy as np
import config as cf
import ui
from ui import MI


bot = telebot.TeleBot(cf.token)

server = Flask(__name__)

Mi = MI(bot)

stack = []
stack_count = 2
do = None

def Stack(_do, message):
    global do
    do = _do
    _stack(None, message)

def _stack(matr, msg):
    global stack
    global do

    Mi.clear()
    Mi.set_on_ok(_stack)

    if matr is not None:
        stack.append(matr)

    if len(stack) < stack_count:
        print("?")
        Mi.input(msg)
    else:
        if callable(do):
            bot.send_message(msg.chat.id, do(stack[0],stack[1]))
            print(do(stack[0],stack[1]))
            stack = []
            do = None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(message.from_user.first_name)
    bot.send_message(message.chat.id, cf.start_msg)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, cf.help_msg)

@bot.message_handler(commands=['input'])
def testinput(message):
    bot.send_message(message.chat.id, "♥")
    Mi.clear()
    Mi.input(message)

@bot.message_handler(commands=['dot'])
def dot(message):
    Stack(lathings.dot, message)

@bot.message_handler(commands=['sum'])
def dot(message):
    Stack(lathings.sum, message)

@bot.message_handler(commands=['stairs'])
def stairs_v2(message):
    Mi.clear()
    Mi.set_on_ok(stairs_next)
    Mi.input(message)

def stairs_next(matr, msg):
    n = matr.shape[0]
    m = matr.shape[1]
    bot.send_message(msg.chat.id, lathings.stairs(n, m, matr))

step = 0
n = 0
m = 0

@bot.message_handler(commands=['to_stairs'])
def to_stairs(message):
    global step
    global n
    global m
    try:
        if step == 0:
            bot.send_message(message.chat.id, "n:")
        if step == 1:
            n = int(message.text)
            bot.send_message(message.chat.id, "m:")
        if step == 2:
            m = int(message.text)
            bot.send_message(message.chat.id, "matr:")
        if step == 3:
            strmatr = message.text.split("\n")
            matr = lathings.from_str(strmatr)
            rrr = lathings.stairs(n, n, matr)
            print(rrr)
            bot.send_message(message.chat.id, rrr)
            step = 0
            return
        bot.register_next_step_handler(message, to_stairs)
        step += 1
    except Exception as e:
        bot.send_message(message.chat.id, e)
        step = 0

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message.from_user.first_name + ": " + message.text)
    new = ""
    text = message.text.lower()
    text = re.sub('[!@#$.,?0-9]', '', text)
    for word in text.split(" "):
        if len(word) > 3:
            new += "хуе" + word[2:] + " "
        else:
            new += word + " "
    new += "."
    bot.reply_to(message, new)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    #обработка ввода матрицы
    Mi.keyboard_callback(call)

@server.route('/' + cf.token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://la-things-bot.herokuapp.com/' + cf.token)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    pass

#bot.remove_webhook()
#bot.polling()
