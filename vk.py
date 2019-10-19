# -*- coding: utf-8 -*-


#TODO: сделать загрузку файлов на сервер,
#TODO: сделать авторизацию



import requests as req
import logging
from sys import stdout
from time import sleep, time, strftime
from random import randint



class vk:
	def __init__(self, token, testing_mode=False, min_wait_time=3, max_wait_time=6, logger_name='vk', log_level='info', api_version=str(5.92)):#20.12 - работает
		self.token = token#token
		self.api_version = api_version#api version
		self.min_wait_time = min_wait_time#to have no_captcha
		self.max_wait_time = max_wait_time#to have no_captcha
		self.TEMP = None#костыль, я знаю, мб к 0.5 исправлю
		self.id = None#Переменные, необходимые для определеия в доч. классах
		self.start_time = int(time())
		self.testing_mode = testing_mode
		self.stub = {'error': {'error_code': 'stub', 'request_params':[{'key': 'method', 'value':'stub.stub'}, {'key': 'v', 'value': '5.92'}]}}
		#хз зачем это говно, по идее заглушка

		#логгер
		self.log = logging.getLogger(logger_name)

		if not len(self.log.handlers):
			if log_level == 'debug': log_level = logging.DEBUG
			elif log_level == 'info': log_level = logging.INFO
			elif log_level == 'warning': log_level = logging.WARNING
			elif log_level == 'error': log_level = logging.ERROR
			elif log_level == 'critical': log_level = logging.CRITICAL
			handler = logging.StreamHandler(stdout)
			handler.setFormatter(logging.Formatter("%(asctime)s - [%(name)s][%(levelname)s]: %(message)s"))
			self.log.addHandler(handler)
			handler = logging.FileHandler('logs.log')
			formatter = logging.Formatter('%(asctime)s - [%(name)s][%(levelname)s]: %(message)s')
			handler.setFormatter(formatter)
			self.log.addHandler(logging.FileHandler('logs.log'))
			self.log.setLevel(log_level)
			self.log.info('S T A R T\n')

			

	def jsoner(self, data):#20.12 - работает
		#Эта функция обрабатывает входящий, сырой response обьект и делает из него что-то понятное
		#было: {error:{'error_code': '14', 'lol':'lol228'}} стало: {'error_code': 'captcha', 'lol':'lol228'}
		#чтобы проверить, ошибка ли это, проверьте error code

		data = data.json()

		if data.get('error') != None:
			
			if data.get('error').get('error_code') == 14:
				data['error']['error_code'] = 'capthca'
			if data.get('error').get('error_code') == 100:
				data['error']['error_code'] = 'params'
			if data.get('error').get('error_code') == 7:
				data['error']['error_code'] = 'not_root'
			if data.get('error').get('error_code') == 6:
				data['error']['error_code'] = 'too_much_requests'
			if data.get('error').get('error_code') == 18:
				data['error']['error_code'] = 'user_blocked'
			if data.get('error').get('error_code') == 'stub':
				self.log.critical('hey there jsoner(), we got stub!')
				raise RuntimeError('we got stub')
			self.log.error('vk sent error: ' +str(data.get('error').get('error_code')))
			self.log.debug(data.get('error'))
			#дебаг патамуша в дочерней функции все должно обьясняться без голого запроса

			return data.get('error')
			#TODO: добавить еще этих ошибок, пока вроде достаточно

		else:
			return data.get('response')


	def method(self, method, args, captcha_id = '', captcha_key = ''):#20.12 - работает
		#эта дичь просто посылает запрос на сервер вк, собирая нужную ссылку по частям.
		
		url = 'https://api.vk.com/method/' + method + '?'
		if self.testing_mode == True:
			url = 'http://localhost:22824/?'

		for i in args.keys():
			url = url + i + '=' + str(args.get(i)) + '&'#adding every arg we have
		url = url + 'access_token=' + self.token +'&v=' + str(self.api_version)#adding version and token
		
		if captcha_id != '':
			url = url + '&captcha_id=' + str(captcha_id) + '&captcha_key=' + str(captcha_key)
		
		return req.post(url)


	def get_group_members(self, group_id, sort = 'id_asc'):#20.12 - работает
		#закидывает вам участников группы, которую вы укажите.
		params = {'group_id': group_id, 'sort': sort}
		r = self.jsoner(self.method('groups.getMembers', params))
		
		try: members = r.get('items')
		except AttributeError: self.log.error('ERROR! '+self.get_group_members.__name__+', resp:\n' + r);return r
		except LookupError: self.log.error('ERROR! '+self.get_group_members.__name__+', resp:\n' + r);return r
		
		return members


	def get_usrinfo(self, url, fields= None):#20.12 - работает
		#дает инфу о пользователе
		try:
			int(url)#если юрл не число, а ссылка - тогда выполняем исключение
		except TypeError:

			url = str(url)
			if url.find('?') != -1:
				url = url[url.find('https://vk.com/')+15:url.find('?')]
			else:
				url = url[url.find('https://vk.com/')+15:len(url)]#deleting everything exept screen name (like vk.com/durov->durov)
			if url.find('id') != -1:#if it was a number, deleting the id prefix (id0000->0000)
				url = url[2:len(url)]

		finally:
			params = {'user_ids': url, 'fields': fields}
			r= self.jsoner(self.method('users.get', params))#эта функция для одного целовека онли
			try: 
				if r.get('error_code') != None: self.log.error('Error - we can not find dude with id ' + str(url))
				
			except AttributeError: self.log.info('get_usrinfo - ok!'); r=r[0]

			return r


	def get_last_posts(self, owner_id, post_count = 100, offset = 1):#20.12 - работает
		#последние посты со стены
		self.log.info('getting last posts from wall...')
		arr = []
		params = {'count': post_count, 'owner_id': owner_id, 'offset': offset}
		r=self.jsoner(self.method('wall.get', params))
		arr=[i for i in r.get('items')]
		return arr


	def post(self, owner_id, msg ='ыыы', attachments='', time='', from_group='', is_ad=''):#20.12 - работает
		#публикует запись на стене
		params={'owner_id': owner_id, 'attachments': attachments, 'message': msg,'publish_date': time, 'from_group': from_group, 'guid': randint(0, 100000), 'marked_as_ads': is_ad}
		self.log.info('posting something...')
		return self.jsoner(self.method('wall.post', params))

	def add_friend(self, id, msg=''):#20.12 - работает
		#добавляет друга
		params = {'user_id': id, 'text': msg}#it should be text, not 'message'. idk also.
		self.log.debug('adding friend...')
		return self.jsoner(self.method('friends.add', params))

	def get_friends(self, id, offset =0):##20.12 - работает
		# возвращает список друзей человека
		params = {'user_id': id, 'offset': offset}
		r= self.jsoner(self.method('friends.get', params)).get('items')
		return r


	def msg(self, msg, id):#20.12 - работает
		#отправляет сообщение человеку
		params = {'message': msg, 'user_id': self.get_usrinfo(id).get('id')}
		self.log.debug('sending message...')
		r=self.jsoner(self.method('messages.send', params))
		return r

	def comment(self, owner_id, post_id, msg, attachments = '', from_group = ''):#20.12 - работает
		#оставить комментарий под постом
		params = {'owner_id': owner_id, 'post_id': post_id, 'attachments': attachments, 'message': msg, 'from_group': from_group}
		self.log.debug('sending comment...')
		return self.method('wall.createComment', params)
		
	def get_rand_ids(self, count, last_seen_days_max = 3, start_id = 1):#20.12 - работает
		#выдает тебе рандомные айдишники активных пользователей
		#минимальное кол-во юзеров: 100

		self.log.info('started get_rand_ids')
		
		real_count = 1000
		offset = randint(0, 5500000)
		params = {'user_id': start_id, 'count': real_count, 'offset': offset, 'fields': 'last_seen,can_write_private_message'}
		data = self.jsoner(self.method('users.getFollowers', params))
		
		if data.get('error') != None:
			self.log.error('getting_rand_ids, critical\nresponse: '+data)
			return [1]
			
		data = data.get('items')
		i=0
		removed = 0
		while True:
			deffective = False
			try: data[i+1]
			except:
				self.log.warning('Adding 1000 ppl to data, cuz last time it wasnt enough')
				sleep(0.4)
				params['offset'] = params['offset']+real_count
				data = data+self.jsoner(self.method('users.getFollowers', params)).get('items')
			usr=data[i]
			
			if usr.get('deactivated') != None:#some shit, where we check activity of user.
				data.remove(usr)
				removed+=1
				self.log.debug(str(usr.get('id'))+' has been removed of he\'s deactivated, totaly: ' + str(removed))
				continue
			if usr.get('last_seen').get('time')+259200 < self.start_time:
				data.remove(usr)
				removed+=1
				self.log.debug(str(usr.get('id'))+' has been removed of he\'s not last_seen recently, totaly: ' + str(removed))
				continue
			if usr.get('can_write_private_message') == 0:
				data.remove(usr)
				removed+=1 
				self.log.debug(str(usr.get('id'))+' has been removed of he has closed msges, totaly: ' + str(removed))
				continue

			i+=1
			if len(data) >= count:
				for i in range(0, len(data)-count):
					#remove extra ids
					data.pop()
				break

		data = [i.get('id') for i in data]
		self.log.info('found '+str(count)+' ids, during operetion ' + str(removed)+ ' has been removed')
		return data







	# def upload_photo(self, album_id, photos, group_id = '', capition=''):
	# 	#пока не работает, но должно загружать фото на сервер

	# 	#TODO: finally make it work
	# 	url=self.method('photos.getUploadServer', {'album_id': album_id, 'group_id': group_id}).get('response').get('upload_url')#having url
	# 	r=req.post(url, files=photos)#making request to this url
	# 	r=self.method('photos.saveWallPhoto', {'user_id': group_id, 'photo': r.get('response'),
	# 	'hash': r.get('response'), 'server': r.get('response'), 'capition': capition})#saving photo

	# 	return r



	# def enter_captcha(self, url, r, additional=[]):#TODO: use tk.py file, app class.
	# 	pic = req.get(url, stream = True)
	# 	jpeg_pic =''
	# 	with open('captcha.jpg', 'wb') as fd:
	# 		for chunk in pic.iter_content(chunk_size=128):#TODO: write at var directly, not via saving it to file.
	# 			fd.write(chunk)#saving capthca picture to file
	# 			jpeg_pic = jpeg_pic + chunk

	# 	def captcha_sender(r, captcha_key):#TODO: fix ЏРєРёР symbols.
	# 		resp=r[1]#TODO: fix this shit and use method() instead
	# 		url = 'https://api.vk.com/method/' + resp.get('request_params')[1].get('value') + '?'#adding method
	# 		url=url+'captcha_sid='+resp.get('captcha_sid')+'&captcha_key='+captcha_key + '&access_token=' + self.token +'&v=' + self.api_version
	# 		for i in additional:
	# 			url = url +'&'+ i[0].decode('utf-8')+ '=' + i[1].decode('utf-8')
	# 		for i in resp.get('request_params'):#getting info
	# 			url = url + '&' + i.get('key') +'='+ i.get('value')
	# 		self.TEMP = self.jsoner(req.post(url))
		

	# 	root=tk.Tk()
	# 	captcha = tk.StringVar()
	# 	captcha.set('')
	# 	img = ImageTk.PhotoImage(Image.open('captcha.jpg'))
	# 	panel = tk.Label(root, image = img)
	# 	panel.pack()

	# 	entry_field = tk.Entry(root, textvariable=captcha)
	# 	entry_field.bind("<Return>", lambda a=1,captcha=captcha: captcha_sender(r, captcha.get()))
	# 	ok = tk.Button(root,text= "Send", command= lambda a=1,captcha=captcha: captcha_sender(r, captcha.get()))#command=captcha_url_maker
	# 	entry_field.pack()
	# 	ok.pack()

	# 	while True:
	# 		root.update()

	# 		if self.TEMP != None:
	# 			root.destroy()
	# 			tmp = self.TEMP
	# 			self.TEMP=None
	# 			return tmp
