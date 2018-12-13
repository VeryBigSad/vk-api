# -*- coding: utf-8 -*-


#TODO: сделать загрузку файлов на сервер,
#TODO: сделать авторизацию

#TODO: разделить все на 3 файла: просто гет функции, хуйня для спама и хуйня для групп-бота
#СРОЧНО: адаптировать все говно под новый джсонер, или нахуй его в печку


import requests as req
import json
import time
import random



class vk:
		def __init__(self, token, min_wait_time=3, max_wait_time=6, type='bot', api_version=5.90):
		self.type = type#type of user - bot, group, etc
		self.token = token#token
		self.api_version = api_version#api version
		self.min_wait_time = min_wait_time#to have no_captcha
		self.max_wait_time = max_wait_time#to have no_captcha
		self.TEMP = None#костыль, я знаю, мб к 0.5 исправлю
		self.id = self.method('users.get', {}, token).json().get('response')[0].get('id')

	def jsoner(self, data):
		#Эта функция обрабатывает входящий, сырой response обьект и делает из него что-то понятное
		#во всяком случае так задумывалось


		#TODO: обязательно сделать! крч если все ок то он все оставляет иначе он заменяет
		#      поле с кодом ошибки на ключевое слово, например capthca или privacy
		data = data.json() 
		if data.get('error') != None:

			if data.get('error').get('error_code') == 14:
				return {'error': {'type': 'captcha', 'resp': data.get('error')}}
			elif data.get('error').get('error_code') == 902:
				return {'error': {'type': 'privacy', 'resp': data.get('error')}}
			else:
				return {'error': {'type': 'unknown', 'resp': data.get('error')}}
		
		else:
			return {'response': {'resp': data.get('response')}}

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
		r = jsoner(method('groups.getMembers', params))
		if r.get('error') != None: return r
		r = r.get('response').get('resp')

		for i in range(0, len(r.get('items'))):
			members = r.get('items')
		return members


	def get_usrinfo(self, url, fields = None):
		#дает инфу о пользователе
		try:
			str(url) == int(url)#it works. dont touch it.
		except BaseException:

			url = str(url)
			if url.find('?') != -1:
				url = url[url.find('https://vk.com/')+15:url.find('?')]
			else:
				url = url[url.find('https://vk.com/')+15:len(url)]#deleting everything exept screen name (like vk.com/durov->durov)
			if url.find('id') != -1:#if it was a number, deleting the id prefix (id0000->0000)
				url = url[2:len(url)]

		#TODO: use needed parametr
		params = {'user_ids': url}
		return jsoner(method('users.get', params)) #post->json->'response'->list->our dict(we return it)


	def get_last_posts(self, group_id, post_count = 100, offset = 1):
		#последние посты со стены группы
		arr = []
		params = {'count': post_count, 'owner_id': group_id, 'offset': offset}
		r=jsoner(method('wall.get', params))
		if type(r) is list:#TODO: убрать нахуй это говно, использовать пока еще не написанный джсонер
			return r

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
		return jsoner(method('friends.add', params))

	def get_friends(self, id, offset =0):#returns list of friends
		# возвращает список друзей человека
		params = {'user_id': id, 'offset': offset}
		r= jsoner(method('friends.get', params)).get('items')
		return r


	def msg(self, msg, id):
		#отправляет сообщение человеку
		params = {'message': msg, 'user_id': get_usrinfo(id).get('id'),'random_id': abs(hash(msg)) % (10 ** 8)}
		r=jsoner(method('messages.send', params))
		return r

	def comment(self, owner_id, post_id, msg, attachments = '', from_group = ''):
		#оставить комментарий под постом
		params = {'owner_id': owner_id, 'post_id': post_id, 'attachments': attachments, 'message': msg, 'from_group': from_group}
		return jsoner(method('wall.createComment', params))

	def group_ban(self, id, group_id, token, comment = 'Видимо, вы сделали что-то ужасное.', reason=None,comment_visible = 1, time = None):
		#бан в группе выдает
		params = {'owner_id': id, 'group_id': group_id, 'comment': comment, 'comment_visible': comment_visible}
		if reason != None:
			params.formkeys('reason', reason)
		if time != None:
			params.formkeys('end_time', time)
		return method('groups.ban', params, token).text
		
	def get_rand_ids(self, count, last_seen_days_max = 3, start_id = 1):
		#выдает тебе рандомные айдишники активных пользователей
		#TODO: сделать проверку на то, можно ли писать
		real_count=1000
		offset = random.randint(0, 5500000)
		params = {'user_id': start_id, 'count': real_count, 'offset': offset, 'fields': 'last_seen'}
		
		data = jsoner(method('users.getFollowers', params))
		if data.get('error') != None: return data

		data = data.get('response').get('resp').get('items')
		i=0

		while True:
			deffective = False
			usr=data[i]
			
			if usr.get('deactivated') != None:#some shit, where we check activity of user.
				data.remove(usr)
				continue
			if usr.get('last_seen').get('time')+259200 < time:
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
				data = data + jsoner(method('users.getFollowers', params)).get('items')

		data = [i.get('id') for i in data]
		return data




	def upload_photo(self, album_id, photos, group_id = '', capition=''):
		#пока не работает, но должно загружать фото на сервер
		
		#TODO: finally make it work
		url=method('photos.getUploadServer', {'album_id': album_id, 'group_id': group_id}).get('response').get('upload_url')#having url
		r=req.post(url, files=photos)#making request to this url
		r=method('photos.saveWallPhoto', {'user_id': group_id, 'photo': r.get('response'),
		'hash': r.get('response'), 'server': r.get('response'), 'capition': capition})#saving photo

		return r #NOT FINISHED!


