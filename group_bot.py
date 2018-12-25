# -*- coding: utf-8 -*-

from vk import *
from sys import path
path.insert(0, 'callback')
import message_handler

class group(vk):
	def __init__(self, token, id=174145768, testing_mode=False, min_wait_time=3, max_wait_time=6,logger_name='vk', log_level='info', api_version=5.90):
		vk.__init__(self, token, testing_mode,min_wait_time, max_wait_time,logger_name,log_level, api_version)
		self.id = id
		self.log.info('Group class started!')


	def ban(self, id, group_id, comment = 'Видимо, вы сделали что-то ужасное.', time = None,reason=None,comment_visible = 1):
		#бан в группе выдает
		params = {'owner_id': id, 'group_id': group_id, 'comment': comment, 'comment_visible': comment_visible}
		if reason != None:
			params.formkeys('reason', reason)
		if time != None:
			params.formkeys('end_time', time)
		self.log.debug('banning ' + id+'...')
		return jsoner(self.method('groups.ban', params, token))


	def mass_ban(self, ids, comment = 'ы', time = None):
		#тоже самое что и выше, только большому кол-ву людей
		for id in ids:
			self.group_ban(id, self.id, comment, time)
	

	def msg_spammer(self, ids):
		#спамит сообщениями людям, указанным в ids (это лист)
		id_list = ''
		for j in range(1, len(ids)/100):
			for i in range((j-1)*100, j*100-1):
				id_list = id_list + str(ids[i]) + ','#converting them to a string id1 + ',' + id2 + ','...
				if ids[i+1] == None: break
			id_list = id_list[0:len(id_list)-1]#delete the last ',' point

			params = {'message': msg, 'user_ids': id_list, 'random_id': abs(hash(msg)) % (10 ** 8)}
			response = self.jsoner(self.method('messages.send', params))
			sleep(randint(self.min_wait_time,self.max_wait_time))
	def start_callback(self):
		callback.run(host='0.0.0.0', port='22823')

