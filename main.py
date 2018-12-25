# -*- coding: utf-8 -*-


#крч, вот мне на завтра задание - как только закончу дрочить на каллбак, проетстить все функции и отправить в /master
#а то это рили пиздец



<<<<<<< HEAD
from settings import *
import group_bot
import vk_bot

import Tkinter

def main():
=======

import group_bot
import vk_bot
from time import *
from flask import *

def main():
	###ENTER TOKENS BELOW
	###ENTER TOKENS BELOW
	###ENTER TOKENS BELOW
	group_token = ''#group
	bot_token   = ''#bot

>>>>>>> d77cf3d6930fca8dc67cceb26102a0f3f35af76b

	bot = vk_bot.bot(bot_token)#инициализируем обьекты с нашими токенами
	group = group_bot.group(group_token)

if __name__ == '__main__':
	main()


