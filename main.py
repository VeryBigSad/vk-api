# -*- coding: utf-8 -*-
import vk
import vk_callback

def main():
	main_account_token = 'cf1c53684ad5c8fed7d87a3ec5ecbdad43d8efcf78faab9f2cd1c41852a2d1f2839f2c1bf34c3b1ef2117'#account 1
	group_token = '3e43264dcb39c26b2b9f86902c878f12897ba0b842331eb9340f6d0315d119f6e8095093de2b802d78432'#group mrb
	bot_token = 'e84a6420bbde0273488e16dea2228699a620ded0c9504f0945c91e4c4cebaac2848bb464edea2ce1e1c9e'#bot

	main = vk.vkapi(main_account_token, -174145768,5,15)#DO NOT EVER TOUCH IT UROD
	group = vk.vkapi(group_token, -174145768,3,6, type='group')
	bot = vk.vkapi(bot_token, -174145768,5,8)
	#group_bot = vk_callback.vk()
	#print(bot.add_friends(bot.get_rand_ids(1)[0], 19))
	group.msg_spammer('Приветик!) Пожалуйста, порепости пару мемасиков с нашего паблоса, это нам очень поможет c:', group.get_group_members(174145768))

if __name__ == '__main__':
	main()

