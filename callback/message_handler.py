# -*- coding: utf-8 -*-
import words
from sys import path
path.insert(0, '../')#not working, fix it
#aaaaaaaaaaaa
from vk import *

def msg_handler(data):
	if data.get('secret') != secret_word: return 'not vk'#проверяем, вк ли это вообще.

	group.msg('[id' + str(data.get('object').get('id'))+'|'+str(group.get_usrinfo(data.get('object').get('id'))).get('first_name')+str(group.get_usrinfo(data.get('object').get('id'))).get('last_name')+']'
		+ ' сделал '+ data.get('object').get('type') + ', вот содержимое:' + data.get('object').get('text'), '516131573')
	#that was logging, sending to my and felix's accounts.


def setting_master(msg): 
	if msg[0] == '!':return False
	msg = msg[1:len(msg)]
	#преобразование в массив с аргументами
	args = [msg.split(' ')]#получили массив с аргументами
	admin_commands=['команды', 'забанить', 'отключить_бота']
	usr_commands=['']

setting_master('!asd')
