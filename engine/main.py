# -*- coding: utf-8 -*-


#крч, вот мне на завтра задание - как только закончу дрочить на каллбак, проетстить все функции и отправить в /master
#а то это рили пиздец



from settings import *
import group_bot
import vk_bot

import Tkinter

def main():


	bot = vk_bot.bot(bot_token, log_level='info', logger_name='bot')#инициализируем обьекты с нашими токенами
	main = vk_bot.bot(main_account_token, log_level='info', logger_name='main_account')
	group = group_bot.group(group_token, log_level='info', logger_name='group', group_admin=main)
	group.msg('privet', 522603056)
if __name__ == '__main__':
	main()


