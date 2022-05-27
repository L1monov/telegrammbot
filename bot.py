import telebot
from telebot import types
import logging
import json



bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=["start"])
def start(message): # приветсвие пользователя
	mess = f'Hello, <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
	bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['admin']) #Админ панель
def admin(message):
	with open('baza.json', 'r') as file:
		file = json.load(file)
	if message.from_user.id in file['admins']: # Проверка на админку
		bot.send_message(message.chat.id, 'You admin')
		markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=2)
		edit = types.KeyboardButton('Редакция слов для отправки')
		something = types.KeyboardButton('Что то еще')
		markup.add(edit,something)
		bot.send_message(message.chat.id, 'Что хочешь?', reply_markup=markup)
	elif message.from_user.id not in file['admins']:
		bot.send_message(message.chat.id, 'Ты не админ :(')
@bot.message_handler(commands=['id']) 
def id(message): #Отправлет айди пользователя
	bot.send_message(message.chat.id,f'Your ID: {message.from_user.id}')
	bot.send_message(IdAmind,f'Your ID: {message.from_user.id}')
@bot.message_handler(content_types=['text']) # Обработка сообщений
def get_text(message):
	with open('baza.json', 'r', encoding='utf-8') as file:
		file = json.load(file)
	if message.text.lower() in file["wordstosend"]: # Проверка на отправку слов
		bot.send_message(IdAmind, f'Пришла заявка на дизайн от : {message.from_user.first_name}.')
	if message.text == 'Редакция слов для отправки': # Редакция слов на отправку (Для админов)
		markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=2)
		words = types.KeyboardButton('Посмотреть слова')
		add = types.KeyboardButton('Добавить')
		remove = types.KeyboardButton('Удалить')
		markup.add(words, add,remove)
		bot.send_message(message.chat.id, 'Выбери действие', reply_markup=markup)
	elif message.text == 'Добавить':		# Добавление слов ( Для админа )
		send = bot.send_message(message.chat.id, 'Введите слово для добавления:')
		bot.register_next_step_handler(send, add_word)

	elif message.text == 'Да':
		bot.send_message(message.chat.id, f' Добавляенно')
		markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=2)
		words = types.KeyboardButton('Посмотреть слова')
		add = types.KeyboardButton('Добавить')
		remove = types.KeyboardButton('Удалить')
		markup.add(words, add,remove)
		bot.send_message(message.chat.id, 'Выбери действие', reply_markup=markup)
def add_word(message): # Добавление слов в базу
	markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=2)
	yes = types.KeyboardButton('Да')
	no = types.KeyboardButton('Нет')
	markup.add(yes, no)
	bot.send_message(message.chat.id, f'Хотите добавить: {message.text}?', reply_markup=markup)
	with open('baza.json', 'r',encoding='utf-8') as file:
		a = json.load(file)
	a ["wordstosend"].append(message.text.lower())
	
	with open('baza.json', 'w',encoding='utf-8') as file:
		json.dump(a, file, indent =4,ensure_ascii=False)


bot.polling(none_stop=True)
