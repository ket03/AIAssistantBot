import telebot
from os import getenv
from openai import OpenAI

from dotenv import load_dotenv
from telebot.types import LabeledPrice

from Keyboard import kb, kb_payment
from db import create_table, add_user, change_value_stars, set_stars_to_zero, sub_value_counter, change_value_model, \
    change_value_counter, get_value_stars, select_table, is_enough_counter, get_value_model, get_value_counter


'''-------------------------------------------SETUP------------------------------------'''


load_dotenv()
create_table()
bot = telebot.TeleBot(getenv('TOKEN'), parse_mode='Markdown')
client = OpenAI(
    api_key=getenv('OPENAI'),
    base_url=getenv('BASE_URL')
)


'''--------------------------------------------------------------------------------------'''


'''-----------------------------Payment functionality------------------------------------'''


@bot.callback_query_handler(func=lambda call: call.data in ['1', '5', '100', '250', '500', '1000'])
def handle_payment(call):
    set_stars_to_zero(call.message.chat.id)
    amount = int(call.data)
    prices = [LabeledPrice(label='XTR', amount=amount)]
    bot.send_invoice(call.message.chat.id,
                     title='Subscribe to AI',
                     description='✨ After subscribe, bot will communicate with you ✨',
                     invoice_payload='sub_purchase_payload',
                     provider_token='',
                     currency='XTR',
                     prices=prices)

    change_value_stars(call.message.chat.id, amount)
    select_table()
    bot.answer_callback_query(call.id)


@bot.pre_checkout_query_handler(func=lambda query: True)
def handle_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    current_stars = get_value_stars(message.chat.id)
    change_value_counter(message.chat.id, current_stars)
    set_stars_to_zero(message.chat.id)
    select_table()

    bot.send_message(message.chat.id,'✨ You have successfully paid for your subscription! 🌟\n'
                                'Thank you for your support! 🎉 Now bot can communicate with you! ✨\n\n'
                     'Now you have ' + str(get_value_counter(message.chat.id)) + ' requests')


'''----------------------------------------------------------------------------------------------'''


'''-----------------------------Message handlers -------------------------------------------------'''


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     text='🤖 I am an AI-assistant. I help both school and college students also employees with their tasks.\n\n'
                          'I can:\n'
                          '🔍 1) Find information\n'
                          '📚 2) Explain something in simple words\n'
                          '📝 3) Write a report\n'
                          '🧮 4) Solve a math problem\n'
                          '📖 5) Retell a summary of a piece of literature\n\n'
                          '🌟 And many other things up to help in choosing a car.\n'
                          '✨ My possibilities are limited only by your imagination\n\n'
                          '⚠️ Just remember, I am just a tool. If the topic of the question requires deep knowledge, it is better to check the information for reliability\n'
                          '⚠️ He has not context!!! he does not memorize conversations\n\n'
                     '✨!!!Price - 10 star = 1 request!!!✨\n\n\n'
                     '!!!Also you can use image generator DALL-E-3. 50 star = 1 request!!!',
                     reply_markup=kb)

    add_user(message.chat.id)
    select_table()


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    current_model = get_value_model(message.chat.id)
    current_counter = get_value_counter(message.chat.id)
    if is_enough_counter(current_model, current_counter):
        sub_value_counter(message.chat.id, current_model)
        if current_model == 'gpt-4o':
            gpt_request(message)
        elif current_model == 'dalle':
            dalle_request(message)
    else:
        bot.send_message(message.chat.id, 'You must to top up balance')
    select_table()


def gpt_request(message):
    user_response =  message.text
    stream = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {"role": "system", "content": "Max token is 1000, use only text markup Markdown"},
            {"role": "user", "content": user_response}
        ],
        stream=True
    )

    counter_chunk = 0
    buffer = ''
    sent_message = bot.send_message(message.chat.id, '#')
    for chunk in stream:
        reserve_buffer = chunk.choices[0].delta.content
        if reserve_buffer != '':
            buffer += reserve_buffer
            counter_chunk += 1
        if counter_chunk >= 20:
            bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text=buffer)
            counter_chunk = 0
    if counter_chunk > 0:
        bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text=buffer)


def dalle_request(message):
    user_response = message.text
    response = client.images.generate(
        model="dall-e-3",
        prompt=user_response,
        size="1024x1024",
        quality="standard",
        n=1
    )
    bot.send_message(message.chat.id, response.data[0].url)


'''----------------------------------------------------------------------------------------------'''


'''-----------------------------Button handlers--------------------------------------------------'''


@bot.callback_query_handler(func=lambda call: call.data == 'top_up')
def callback_top_up_query(call):
    bot.send_message(call.message.chat.id, 'Choose tariff(10 stars✨ per request):', reply_markup=kb_payment)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data in ['gpt-4o', 'dalle'])
def callback_choose_model_query(call):
    if call.data == 'gpt-4o':
        change_value_model(call.message.chat.id, call.data)
    if call.data == 'dalle':
        change_value_model(call.message.chat.id, call.data)
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 'Model changed to - ' + call.data)


'''----------------------------------------------------------------------------------------------'''


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()