# -*- coding: utf-8 -*-


#крч, вот мне на завтра задание - как только закончу дрочить на каллбак, проетстить все функции и отправить в /master
#а то это рили пиздец



from settings import *
import group_bot
import vk_bot

import Tkinter

def main():

	bot = vk_bot.bot(bot_token)#инициализируем обьекты с нашими токенами
	group = group_bot.group(group_token)

if __name__ == '__main__':
	main()


