from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

'''Start keyboard'''
kb = InlineKeyboardMarkup()
btn_gpt = InlineKeyboardButton('Gpt-4o', callback_data='gpt-4o')
btn_midj = InlineKeyboardButton('Dalle', callback_data='dalle')
btn_top_up = InlineKeyboardButton('Top up your balance', callback_data='top_up')
kb.add(btn_gpt, btn_midj)
kb.add(btn_top_up)

'''Payment keyboard'''
kb_payment = InlineKeyboardMarkup(row_width=2)
btn_pay_1 = InlineKeyboardButton('1✨', callback_data='1')
btn_pay_2 = InlineKeyboardButton('5✨', callback_data='5')
btn_pay_3 = InlineKeyboardButton('100✨', callback_data='100')
btn_pay_4 = InlineKeyboardButton('250✨', callback_data='250')
btn_pay_5 = InlineKeyboardButton('500✨', callback_data='500')
btn_pay_6 = InlineKeyboardButton('1000✨', callback_data='1000')
kb_payment.add(btn_pay_1, btn_pay_2, btn_pay_3, btn_pay_4, btn_pay_5, btn_pay_6)
