# -*- coding: utf-8 -*-
import telebot, get_data_from_ethermine, get_data_from_https, datetime,registration_module
from additional_data import telegram_token,author_id,default_weather_city_id

debug_level='DEBUG'
_el_typing_time=15
_el_date=str((datetime.date.today()))
_el_token=telegram_token
_bot=telebot.TeleBot(_el_token)

print(_bot.get_me())
_bot.send_message(author_id, 'Bot started' ,parse_mode='HTML')

def _log(message, ans):
    print('\n ----------')
    print(datetime.datetime.now())
    print(message.from_user.first_name)
    print(message.from_user.last_name)
    print(str(message.from_user.id))
    print(message.text)
    print(ans)
    if debug_level=='DEBUG':
        _bot.forward_message(author_id, message.from_user.id, message.message_id)

def _el_action(chat_id, times, action_type):
    for i in range(times):
        _bot.send_chat_action(chat_id, action_type)

@_bot.message_handler(commands=['register'])
def handle_start(message):
    msg = _bot.reply_to(message, 'Enter your token:')
    _bot.register_next_step_handler(msg, process_name_step)
    _log(message, 'registration in progress')

def process_name_step(message):
    try:
        answer=registration_module.write_to_json(message.from_user.id, message.text)
        _bot.send_message(message.from_user.id, answer)
        _log(message, answer)
    except:
        answer='oooops'
        _bot.reply_to(message, answer)
        _log(message, answer)

@_bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup=telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start','/help','/stop')
    user_markup.row('/get_statistics','/get_weather')
    answer='Welcome!'
    _bot.send_message(message.from_user.id,answer , reply_markup=user_markup)
    _log(message, answer)

@_bot.message_handler(commands=['stop'])
def handle_start(message):
    hide_markup=telebot.types.ReplyKeyboardRemove()
    _bot.send_message(message.from_user.id, 'hide keyboard', reply_markup=hide_markup)

@_bot.message_handler(commands=['get_statistics'])
def handle_text(message):
    _el_action(message.chat.id, _el_typing_time, 'typing')
    tele_id=str(message.from_user.id)
    if registration_module.user_dict.get(tele_id)==None:
        ans='please /register'
        _bot.send_message(message.chat.id, ans, parse_mode='HTML')
        _log(message, ans)
    else:
        ethermine_tokens=registration_module.user_dict[tele_id]
        for n in range (0,len(ethermine_tokens)):
            pool=get_data_from_ethermine.get_new_info(ethermine_tokens[n])
            unpaid = pool[1]

            stats=get_data_from_ethermine.get_pool_stats()
            usd=stats[1]

            curs=get_data_from_https.get_curs(_el_date)
            rub_to_usd=curs[1]

            paid=get_data_from_ethermine.ethermine_paid(ethermine_tokens[n])
            try:
                unpaid=float(unpaid)
            except:
                unpaid=0
            try:
                paid=float(paid)
            except:
                paid=0
            total = float(unpaid) + float(paid)
            profit=total*float(usd)*float(rub_to_usd)
            profit=(round(profit,2))


            ans='<b>{}</b>\n\n{}\nPaid: <b>{}</b>\nTotal: <b>{}</b>\n\n{}\n{}\n\nProfit: <b>{:7,.2f}</b> RUB'.format(ethermine_tokens[n],
            pool[0],paid,total,stats[0],curs[0],profit)
            _bot.send_message(message.chat.id, ans,parse_mode='HTML')
            _log(message,ans)

@_bot.message_handler(commands=['get_weather'])
def handle_text(message):
    _el_action(message.chat.id, _el_typing_time, 'typing')
    try:
        ans=get_data_from_https.get_weather_by_city_id(default_weather_city_id)
    except:
        ans='error getting weather'
    _bot.send_message(message.chat.id, ans,parse_mode='HTML')
    _log(message,ans)

@_bot.message_handler(commands=['help'])
def handle_text(message):
    _el_action(message.chat.id, _el_typing_time, 'typing')
    _answer = 'This bot will get statistics from ethermine.org for you\nTo start push /register\nYou can register \
many tokens'
    _bot.send_message(message.chat.id, _answer)
    _log(message,_answer)

@_bot.message_handler(commands=['inline'])
def command_help(message):
    markup = telebot.types.InlineKeyboardMarkup()
    itembtna = telebot.types.InlineKeyboardButton('/help', switch_inline_query="")
    itembtnv = telebot.types.InlineKeyboardButton('v', switch_inline_query="")
    itembtnc = telebot.types.InlineKeyboardButton('c', switch_inline_query="")
    markup.row(itembtna)
    markup.row(itembtnv, itembtnc)
    _bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)


@_bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == '/help':
        print('123')
        _bot.send_message(author_id,'123')

""""
@_bot.message_handler(content_types=['text'])
def handle_text(message):
    _new_msg=message.text
    if _new_msg == 'A':
        _el_action(message.chat.id, _el_typing_time, 'typing')
        _answer='B'
        _bot.send_message(message.chat.id,_answer)
        _log(message,_answer)
    elif _new_msg == 'B':
        _el_action(message.chat.id, _el_typing_time, 'typing')
        _answer = 'A'
        _bot.send_message(message.chat.id, _answer)
        _log(message, _answer)
    else:
        _el_action(message.chat.id, _el_typing_time, 'typing')
        _answer = 'bad game'
        _bot.send_message(message.chat.id, _answer)
        _log(message, _answer)
    print(_new_msg+' '+_answer)

"""



_bot.polling(none_stop=True,interval=0)



