# -*- coding: utf-8 -*-
import telebot, get_data_from_ethermine, get_data_from_https, datetime
from additional_data import telegram_token,author_id

debug_level='DEBUG'
_el_typing_time=15
_el_date=str((datetime.date.today()))
_el_token=telegram_token
_bot=telebot.TeleBot(_el_token)
#_bot=telebot.AsyncTeleBot(_el_token)


print(_bot.get_me())

def _log(message, ans):
    print('\n ----------')
    from datetime import datetime
    print(datetime.now())
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


@_bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup=telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start','/get_weather','/stop')
    user_markup.row('/eth_stats', '/eth_rates', '/eth_all')
    answer='Welcome!'
    _bot.send_message(message.from_user.id,answer , reply_markup=user_markup)
    _log(message, answer)

@_bot.message_handler(commands=['stop'])
def handle_start(message):
    hide_markup=telebot.types.ReplyKeyboardRemove()
    _bot.send_message(message.from_user.id, 'hide keyboard', reply_markup=hide_markup)

@_bot.message_handler(commands=['eth_stats'])
def handle_text(message):
    try:
        ans=get_data_from_ethermine.get_new_info('B5304d577494e21Be4fdb13e603248a4A4c61c28')
    except:
        ans='error getting stats'

    _el_action(message.chat.id,_el_typing_time,'typing')
    _bot.send_message(message.chat.id, ans,parse_mode='HTML')
    _log(message,ans)

@_bot.message_handler(commands=['eth_rates'])
def handle_text(message):
    _el_action(message.chat.id, _el_typing_time, 'typing')
    ans=get_data_from_ethermine.get_pool_stats()
    _bot.send_message(message.chat.id, ans,parse_mode='HTML')
    _log(message,ans)

    ans=get_data_from_https.get_curs(_el_date)
    _bot.send_message(message.chat.id, ans,parse_mode='HTML')
    _log(message,ans)

@_bot.message_handler(commands=['eth_all'])
def handle_text(message):
    _el_action(message.chat.id, _el_typing_time, 'typing')

    pool=get_data_from_ethermine.get_new_info('B5304d577494e21Be4fdb13e603248a4A4c61c28')
    unpaid = pool[1]
    ans=pool[0]

    stats=get_data_from_ethermine.get_pool_stats()
    ans=ans+'\n'+stats[0]
    usd=stats[1]

    curs=get_data_from_https.get_curs(_el_date)
    rub_to_usd=curs[1]
    ans=ans+'\n'+curs[0]

    profit=float(unpaid)*float(usd)*float(rub_to_usd)
    profit=round(profit,2)
    ans=ans+'\n'+str(profit)
    _bot.send_message(message.chat.id, ans,parse_mode='HTML')
    _log(message,ans)

@_bot.message_handler(commands=['get_weather'])
def handle_text(message):
    _el_action(message.chat.id, _el_typing_time, 'typing')
    try:
        ans=get_data_from_https.get_weather_by_city_id(524901)
    except:
        ans='error while getting weather'
    _bot.send_message(message.chat.id, ans,parse_mode='HTML')
    _log(message,ans)

@_bot.message_handler(commands=['help'])
def handle_text(message):
    _el_action(message.chat.id, _el_typing_time, 'typing')
    _answer = 'Вот тут будет крутая справка'
    _bot.send_message(message.chat.id, _answer)
    _log(message,_answer)

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


_bot.send_message(author_id, 'Bot started' ,parse_mode='HTML')


_bot.polling(none_stop=True,interval=0)



