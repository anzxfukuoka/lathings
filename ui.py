from telebot import types
import numpy as np
###############################################

class MI:
    def __init__(self, bot):
        self.n = 0
        self.m = 0
        self.matr = None
        self.bot = bot
        self.curr_x = 0
        self.curr_y = 0
        self.on_ok = None

    def input(self, message):
        self.input_size(message)

    def input_size(self, message):
        try:
            nm = message.text.strip().split(" ")
            if len(nm) != 2:
                raise ValueError
            self.n = int(nm[0])
            self.m = int(nm[1])

            #self.bot.register_next_step_handler(message, self.input_matr)
            self.input_matr(message)
        except ValueError as e:
            self.bot.send_message(message.chat.id, "введите через пробел размерность матрицы \n N x M \n" + str(e))
            self.bot.register_next_step_handler(message, self.input_size)
        pass

    def input_matr(self, message):
        self.matr = np.zeros((self.n, self.m), dtype=int)
        self.send_input_keyboard(message)

    def get_input_keyboard_markup():
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        k1 = types.InlineKeyboardButton(text="1", callback_data="1")
        k2 = types.InlineKeyboardButton(text="2", callback_data="2")
        k3 = types.InlineKeyboardButton(text="3", callback_data="3")
        k4 = types.InlineKeyboardButton(text="4", callback_data="4")
        k5 = types.InlineKeyboardButton(text="5", callback_data="5")
        k6 = types.InlineKeyboardButton(text="6", callback_data="6")
        k7 = types.InlineKeyboardButton(text="7", callback_data="7")
        k8 = types.InlineKeyboardButton(text="8", callback_data="8")
        k9 = types.InlineKeyboardButton(text="9", callback_data="9")
        k0 = types.InlineKeyboardButton(text="0", callback_data="0")
        k_empty = types.InlineKeyboardButton(text=" ", callback_data="_empty")
        k_next = types.InlineKeyboardButton(text="->", callback_data="_next")
        k_prev = types.InlineKeyboardButton(text="<-", callback_data="_prev")
        k_clear = types.InlineKeyboardButton(text="C", callback_data="_clear")
        k_m = types.InlineKeyboardButton(text="-", callback_data="-")
        k_ok = types.InlineKeyboardButton(text="OK", callback_data="_ok")

        keyboard.add(k1, k2, k3, k_clear, k4, k5, k6, k_m, k7, k8, k9, k_ok, k_prev, k0, k_next, k_empty)

        return keyboard

    def send_input_keyboard(self, message):
        keyboard = MI.get_input_keyboard_markup()
        self.bot.send_message(message.chat.id, self.get_text(), reply_markup=keyboard)

    def keyboard_callback(self, call):

        keyboard = MI.get_input_keyboard_markup()

        if call.message:
            if call.data == "_next":
                if self.curr_x < self.m - 1:
                    self.curr_x += 1
                else:
                    self.curr_x = 0
                    if self.curr_y < self.n - 1:
                        self.curr_y += 1
                    else:
                        self.curr_y = 0

            if call.data == "_prev":
                if self.curr_x > 0:
                    self.curr_x -= 1
                else:
                    self.curr_x = self.m - 1
                    if self.curr_y > 0:
                        self.curr_y -= 1
                    else:
                        self.curr_y = self.n - 1

            if call.data == "_clear":
                self.matr[self.curr_y][self.curr_x] = 0

            if call.data == "-":
                self.matr[self.curr_y][self.curr_x] = -self.matr[self.curr_y][self.curr_x]

            if call.data.isdigit():
                self.matr[self.curr_y][self.curr_x] = int(str(self.matr[self.curr_y][self.curr_x]) + call.data)

            try:
                self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=self.get_text(), reply_markup=keyboard)
            except Exception as e:
                print(e) #Bad Request: message is not modified

            if call.data == "_ok":
                self.bot.send_message(call.message.chat.id, "OK!")
                if callable(self.on_ok):
                    self.on_ok(self.matr, call.message)

            print(call.data, self.curr_x, self.curr_y)
        pass

    def _matr_to_str(self):
        if self.matr is not None:
            re = ""
            for i in range(self.n):
                for j in range(self.m):
                    if i == self.curr_y and j == self.curr_x:
                        re += "[" + str(self.matr[i][j]) + "] "
                    else:
                        re += str(self.matr[i][j]) + " "
                re += "\n"
            return re
        else:
            return "♠"

    def get_text(self):
        return self._matr_to_str()

    def set_on_ok(self, func):
        self.on_ok = func

    def clear(self):
        self.n = 0
        self.m = 0
        self.matr = None
        self.curr_x = 0
        self.curr_y = 0
        self.on_ok = None



def get_matr_input_markup():
    # Using the ReplyKeyboardMarkup class
    # It's constructor can take the following optional arguments:
    # - resize_keyboard: True/False (default False)
    # - one_time_keyboard: True/False (default False)
    # - selective: True/False (default False)
    # - row_width: integer (default 3)
    # row_width is used in combination with the add() function.
    # It defines how many buttons are fit on each row before continuing on the next row.

    #markup = types.ReplyKeyboardMarkup(row_width=2)
    #itembtn1 = types.KeyboardButton('a')
    #itembtn2 = types.KeyboardButton('v')
    #itembtn3 = types.KeyboardButton('d')
    #markup.add(itembtn1, itembtn2, itembtn3)

    # or add KeyboardButton one row at a time:
    #markup = types.ReplyKeyboardMarkup()
    #itembtna = types.KeyboardButton('a')
    #itembtnv = types.KeyboardButton('v')
    #itembtnc = types.KeyboardButton('c')
    #itembtnd = types.KeyboardButton('d')
    #itembtne = types.KeyboardButton('e')
    #markup.row(itembtna, itembtnv)
    #markup.row(itembtnc, itembtnd, itembtne)

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    k1 = types.InlineKeyboardButton(text="1", callback_data="1")
    k2 = types.InlineKeyboardButton(text="2", callback_data="2")
    k3 = types.InlineKeyboardButton(text="3", callback_data="3")
    k4 = types.InlineKeyboardButton(text="4", callback_data="4")
    k5 = types.InlineKeyboardButton(text="5", callback_data="5")
    k6 = types.InlineKeyboardButton(text="6", callback_data="6")
    k7 = types.InlineKeyboardButton(text="7", callback_data="7")
    k8 = types.InlineKeyboardButton(text="8", callback_data="8")
    k9 = types.InlineKeyboardButton(text="9", callback_data="9")
    k0 = types.InlineKeyboardButton(text="0", callback_data="0")
    k_empty = types.InlineKeyboardButton(text=" ", callback_data="_empty")
    k_next = types.InlineKeyboardButton(text="->", callback_data="_next")
    k_prev = types.InlineKeyboardButton(text="<-", callback_data="_prev")

    keyboard.add(k1, k2, k3, k4, k5, k6, k7, k8, k9, k_prev, k0, k_next)
    #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="X", reply_markup=keyboard)

    return keyboard
