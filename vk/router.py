# -*- coding: utf-8 -*-

import group_bot
from flask import *

app = Flask('mrb')
confrimation_token = 'e38e3fd0'


type = 'test'
group_token = '3e43264dcb39c26b2b9f86902c878f12897ba0b842331eb9340f6d0315d119f6e8095093de2b802d78432'#group mrb

group = group_bot.group(group_token,174145768, True, logger_name='mrb_router')

@app.route('/', methods=['POST'])
def router():
	data = json.loads(request.data)
	if data.get('secret') != secret_word: return 'not vk'#проверяем, вк ли это вообще.

	if data.get('type') == 'confirmation':
		return confirmation_token

	elif data.get('type') == 'message_new':
		#msg_handler(data)
		group.log.info('message came, handling...')
		group.msg('одмен только настраивает бота\nподожди пж дней так 600', data.get('object').get('user_id'))

	elif data.get('type') == 'message_allow':
		group.msg('ну привет, хех', data.get('object').get('user_id'))
		
	elif data.get('type') == 'wall_reply_delete':
		group.msg('ну ты кончено да, комменты удаляешь\nя советую тебе их вернуть пока не пришел главный одмен', data.get('object').get('user_id'))
	elif data.get('type') == 'group_leave':
		group.msg('вернисб, у нас есть печеньки!1!', data.get('object').get('user_id'))
	elif data.get('type') == 'user_unblock':
		group.msg('господен одмен соизволел тебя разбанить\nбудь мудр, не пиши дичь в коментах или хз за что ты в бане оказался', data.get('object').get('user_id'))
	return 'ok'


app.run(host="0.0.0.0", port="22823")
#просто убрать когда понадобится импортить файл


