# -*- coding: utf-8 -*-


#TODO: сделать загрузку файлов на сервер,
#TODO: сделать авторизацию

#TODO: разделить все на 3 файла: просто гет функции, хуйня для спама и хуйня для групп-бота
#СРОЧНО: адаптировать все говно под новый джсонер, или нахуй его в печку


import requests as req
import logging
from time import sleep, time
from random import randint



class vk:
	def __init__(self, token, min_wait_time=3, max_wait_time=6, log_level='info',api_version=5.90):
		self.token = token#token
		self.api_version = api_version#api version
		self.min_wait_time = min_wait_time#to have no_captcha
		self.max_wait_time = max_wait_time#to have no_captcha
		self.TEMP = None#костыль, я знаю, мб к 0.5 исправлю
		self.id = None#Переменные, необходимые для определеия в доч. классах
		self.start_time = int(time())

		if log_level == 'debug': log_level = logging.DEBUG
		elif log_level == 'info': log_level = logging.INFO
		elif log_level == 'warning': log_level = logging.WARNING
		elif log_level == 'error': log_level = logging.ERROR
		elif log_level == 'critical': log_level = logging.CRITICAL
		self.log = logging.getLogger('vk_class')
		logging.basicConfig(filename='logs.log', level=log_level)

	def jsoner(self, data):
		#Эта функция обрабатывает входящий, сырой response обьект и делает из него что-то понятное
		#было: {error:{'error_code': '14', 'lol':'lol228'}} стало: {'error_code': 'captcha', 'lol':'lol228'}
		#чтобы проверить, ошибка ли это, проверьте error code
		

		data = data.json()

		if data.get('error') != None:
			
			if data.get('error').get('error_code') == 14:
				data['error']['error_code'] = 'capthca'

			if data.get('error').get('error_code') == 7:
				data['error']['error_code'] = 'not_root'
			
			if data.get('error').get('error_code') == 6:
				data['error']['error_code'] = 'too_much_requests'
			return data.get('error')
			#TODO: добавить еще этих ошибок, пока вроде достаточно

		else:
			return data.get('response')

	def method(self, method, args, captcha_id = '', captcha_key = ''):#args is array
		#эта дичь просто посылает запрос на сервер вк, собирая нужную ссылку по частям.
		
		url = 'https://api.vk.com/method/' + method + '?'
		for i in args.keys():
			url = url + i + '=' + str(args.get(i)) + '&'#adding every arg we have
		url = url + '&access_token=' + self.token +'&v=' + str(self.api_version)#adding version and token
		if captcha_id != '':
			url = url + '&captcha_id=' + str(captcha_id) + '&captcha_key=' + str(captcha_key)
		
		return req.post(url)


	def get_group_members(self, group_id, sort = 'id_asc'):
		#закидывает вам участников группы, которую вы укажите.
		params = {'group_id': group_id, 'sort': sort}
		r = self.jsoner(self.method('groups.getMembers', params))
		
		try: members = r.get('items')
		except AttributeError: print('ERROR! '+self.get_group_members.__name__+', resp:\n' + r);return r
		except LookupError: print('ERROR! '+self.get_group_members.__name__+', resp:\n' + r);return r
		
		return members


	def get_usrinfo(self, url, fields = None):
		#дает инфу о пользователе
		try:
			str(url) == int(url)#it works. dont touch it.
		except TypeError:

			url = str(url)
			if url.find('?') != -1:
				url = url[url.find('https://vk.com/')+15:url.find('?')]
			else:
				url = url[url.find('https://vk.com/')+15:len(url)]#deleting everything exept screen name (like vk.com/durov->durov)
			if url.find('id') != -1:#if it was a number, deleting the id prefix (id0000->0000)
				url = url[2:len(url)]

		#TODO: use needed parametr
		params = {'user_ids': url}
		return self.jsoner(self.method('users.get', params)) #post->json->'response'->list->our dict(we return it)


	def get_last_posts(self, group_id, post_count = 100, offset = 1):
		#последние посты со стены группы
		arr = []
		params = {'count': post_count, 'owner_id': group_id, 'offset': offset}
		r=self.jsoner(self.method('wall.get', params))

		for i in range(0, post_count):

			arr.append(r.get('response').get('items')[i].get('id'))
		return arr


	def post(self, owner_id, msg ='ыыы (сполелся)', attachments='', time='', from_group='', is_ad=''):
		#публикует запись на странице группы
		params={'owner_id': owner_id, 'attachments': attachments, 'message': msg,'publish_date': time, 'from_group': from_group, 'guid': randint(0, 100000), 'marked_as_ads': is_ad}
		return jsoner(method('wall.post', params))

	def add_friend(self, id, msg=''):
		#добавляет друга
		params = {'user_id': id, 'text': msg}#it should be text, not 'message'. idk also.
		return self.jsoner(self.method('friends.add', params))

	def get_friends(self, id, offset =0):#returns list of friends
		# возвращает список друзей человека
		params = {'user_id': id, 'offset': offset}
		r= self.jsoner(self.method('friends.get', params)).get('items')
		return r


	def msg(self, msg, id):
		#отправляет сообщение человеку
		params = {'message': msg, 'user_id': get_usrinfo(id).get('id'),'random_id': abs(hash(msg)) % (10 ** 8)}
		r=self.jsoner(self.method('messages.send', params))
		return r

	def comment(self, owner_id, post_id, msg, attachments = '', from_group = ''):
		#оставить комментарий под постом
		params = {'owner_id': owner_id, 'post_id': post_id, 'attachments': attachments, 'message': msg, 'from_group': from_group}
		return self.jsoner(self.method('wall.createComment', params))

	def group_ban(self, id, group_id, token, comment = 'Видимо, вы сделали что-то ужасное.', reason=None,comment_visible = 1, time = None):
		#бан в группе выдает
		params = {'owner_id': id, 'group_id': group_id, 'comment': comment, 'comment_visible': comment_visible}
		if reason != None:
			params.formkeys('reason', reason)
		if time != None:
			params.formkeys('end_time', time)
		return jsoner(self.method('groups.ban', params, token))
		
	def get_rand_ids(self, count, last_seen_days_max = 3, start_id = 1):
		#выдает тебе рандомные айдишники активных пользователей
		#TODO: сделать проверку на то, можно ли писать
		real_count=1000
		offset = randint(0, 5500000)
		params = {'user_id': start_id, 'count': real_count, 'offset': offset, 'fields': 'last_seen,can_write_private_message'}
		
		data = self.jsoner(self.method('users.getFollowers', params))
		if data.get('error') != None:
			return data
		data = data.get('items')
		i=0

		while True:
			deffective = False
			usr=data[i]
			
			if usr.get('deactivated') != None:#some shit, where we check activity of user.
				data.remove(usr)
				continue
			if usr.get('last_seen').get('time')+259200 < self.start_time:
				data.remove(usr)
				continue
			if usr.get('can_write_private_message') == 0:
				data.remove(usr)
				continue

			i+=1
			if len(data) >= count:
				for i in range(0, len(data)-count):
					#remove extra ids
					data.pop()
				break
			else:
				sleep(1)
				#if there not enough ppl add them
				params['offset'] = params['offset']+1000
				data = data + self.jsoner(self.method('users.getFollowers', params)).get('items')

		data = [i.get('id') for i in data]
		return data




	def upload_photo(self, album_id, photos, group_id = '', capition=''):
		#пока не работает, но должно загружать фото на сервер

		#TODO: finally make it work
		url=self.method('photos.getUploadServer', {'album_id': album_id, 'group_id': group_id}).get('response').get('upload_url')#having url
		r=req.post(url, files=photos)#making request to this url
		r=self.method('photos.saveWallPhoto', {'user_id': group_id, 'photo': r.get('response'),
		'hash': r.get('response'), 'server': r.get('response'), 'capition': capition})#saving photo

		return r #NOT FINISHED!



	def enter_captcha(self, url, r, additional=[]):#TODO: use tk.py file, app class.
		pic = req.get(url, stream = True)
		jpeg_pic =''
		with open('captcha.jpg', 'wb') as fd:
			for chunk in pic.iter_content(chunk_size=128):#TODO: write at var directly, not via saving it to file.
				print(chunk)
				fd.write(chunk)#saving capthca picture to file
				jpeg_pic = jpeg_pic + chunk
		print(jpeg_pic)
		def captcha_sender(r, captcha_key):#TODO: fix ЏРєРёР symbols.
			resp=r[1]#TODO: fix this shit and use method() instead
			url = 'https://api.vk.com/method/' + resp.get('request_params')[1].get('value') + '?'#adding method
			url=url+'captcha_sid='+resp.get('captcha_sid')+'&captcha_key='+captcha_key + '&access_token=' + self.token +'&v=' + self.api_version
			for i in additional:
				url = url +'&'+ i[0].decode('utf-8')+ '=' + i[1].decode('utf-8')
			for i in resp.get('request_params'):#getting info
				url = url + '&' + i.get('key') +'='+ i.get('value')
			self.TEMP = self.jsoner(req.post(url))
		

		root=tk.Tk()
		captcha = tk.StringVar()
		captcha.set('')
		img = ImageTk.PhotoImage(Image.open('captcha.jpg'))
		panel = tk.Label(root, image = img)
		panel.pack()

		entry_field = tk.Entry(root, textvariable=captcha)
		entry_field.bind("<Return>", lambda a=1,captcha=captcha: captcha_sender(r, captcha.get()))
		ok = tk.Button(root,text= "Send", command= lambda a=1,captcha=captcha: captcha_sender(r, captcha.get()))#command=captcha_url_maker
		entry_field.pack()
		ok.pack()

		while True:
			root.update()

			if self.TEMP != None:
				root.destroy()
				tmp = self.TEMP
				self.TEMP=None
				return tmp
