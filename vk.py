# -*- coding: utf-8 -*-


#TODO: сделать загрузку файлов на сервер,
#TODO: сделать авторизацию

#TODO: разделить все на 3 файла: просто гет функции, хуйня для спама и хуйня для групп-бота
#СРОЧНО: адаптировать все говно под новый джсонер



import requests as req
from random import randint, seed
from time import sleep, time
import json
import Tkinter as tk#do as another file
from PIL import Image, ImageTk


class vkapi:

	def __init__(self, token, id, min_wait_time = 10, max_wait_time = 30, type='bot', test_id = 516131573, api_version = '5.90'):
		self.type = type#type of user - bot, group, etc
		self.token = token#token
		self.api_version = api_version#api version
		self.test_id = test_id#id where we send all testing messages
		self.min_wait_time = min_wait_time#to have no_captcha
		self.max_wait_time = max_wait_time#to have no_captcha
		self.TEMP = None#костыль, я знаю, мб к 0.5 исправлю
		self.time = time()
		seed()

	def jsoner(self,data):
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
		url = 'https://api.vk.com/method/' + method + '?'
		for i in args.keys():
			url = url + i + '=' + str(args.get(i)) + '&'#adding every arg we have
		url = url + '&access_token=' + self.token +'&v=' + self.api_version#adding version and token
		return req.post(url)


	def get_group_members(self,group_id, sort = 'id_asc'):
		params = {'group_id': group_id, 'sort': sort}
		r = self.jsoner(self.method('groups.getMembers', params))
		if r.get('error') != None: return r
		r = r.get('response').get('resp')

		#TODO: if 100+ ppl, make
		for i in range(0, len(r.get('items'))):
			members = r.get('items')
		return members


	def get_usrinfo(self, url, fields = None):
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
		return self.jsoner(self.method('users.get', params)) #post->json->'response'->list->our dict(we return it)


	def get_last_posts(self,group_id, post_count = 100, offset = 1):
		arr = []
		params = {'count': post_count, 'owner_id': group_id, 'offset': offset}
		r=self.jsoner(method('wall.get', params))
		if type(r) is list:
			return r

		for i in range(0, post_count):
			arr.append(r.get('response').get('items')[i].get('id'))
		return arr


	def post(self, owner_id, msg ='ыыы (сполелся)', attachments='', time='', from_group='', is_ad=''):
		params={'owner_id': owner_id, 'attachments': attachments, 'message': msg,'publish_date': time, 'from_group': from_group, 'guid': randint(0, 100000), 'marked_as_ads': is_ad}
		return self.jsoner(self.method('wall.post', params))

	def add_friend(self, id, msg=''):
		params = {'user_id': id, 'text': msg}#it should be text, not 'message'. idk also.
		return self.jsoner(self.method('friends.add', params))

	def get_friends(self, id, offset =0):#returns list of friends
		params = {'user_id': id, 'offset': offset}
		r= self.jsoner(self.method('friends.get', params)).get('items')
		return r


	def msg(self,msg, id):
		params = {'message': msg, 'user_id': self.get_usrinfo(id).get('id'),'random_id': abs(hash(msg)) % (10 ** 8)}
		r=self.jsoner(self.method('messages.send', params))
		return r

	def comment(self,owner_id, post_id, msg, attachments = '', from_group = ''):
		params = {'owner_id': owner_id, 'post_id': post_id, 'attachments': attachments, 'message': msg, 'from_group': from_group}
		return self.jsoner(method('wall.createComment', params))
		
	def get_rand_ids(self, count, last_seen_days_max = 3, start_id = 1):#TODO: TODOOOOOOOOOOOOOOOOOOOO
		real_count=1000
		offset = randint(0, 5500000)

		params = {'user_id': start_id, 'count': real_count, 'offset': offset, 'fields': 'last_seen'}
		data = self.jsoner(self.method('users.getFollowers', params))
		if data.get('error') != None: return data
		data = data.get('response').get('resp').get('items')
		i=0
		while True:
			deffective = False
			usr=data[i]
			
			if usr.get('deactivated') != None:#some shit, where we check activity of user.
				data.remove(usr)
				continue
			if usr.get('last_seen').get('time')+259200 < self.time:
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


	def upload_photo(self, album_id, photos, group_id = '', capition=''):#TODO: finally make it work
		url=self.method('photos.getUploadServer', {'album_id': album_id, 'group_id': group_id}).get('response').get('upload_url')#having url
		r=req.post(url, files=photos)#making request to this url
		r=self.method('photos.saveWallPhoto', {'user_id': group_id, 'photo': r.get('response'),
		'hash': r.get('response'), 'server': r.get('response'), 'capition': capition})#saving photo

		return r #NOT FINISHED!

###########################################################################################################################################################################################################
###########################################                               HERE COMES THE HARD CODE, NOT ONLY FREAKIN EZ FUNCTIONS                               ###########################################
###########################################################################################################################################################################################################

	#HERE WE DONT USE JSONER




	def msg_spammer(self,msg, ids):
		id_list = ''#list of id's (like 1123323,142334,534756 etc)
		r=[]

		if self.type == 'group':#there we can send 100 messages as one request
			for j in range(1, 2):
				for i in range(0,(len(ids))*j):
					id_list = id_list + str(ids[i]) + ','#converting them to a string id1 + ',' + id2 + ','...
				id_list = id_list[0:len(id_list)-1]#delete the last ',' point

				params = {'message': msg, 'user_ids': id_list, 'random_id': abs(hash(msg)) % (10 ** 8)}
				response = self.jsoner(self.method('messages.send', params))
				sleep(randint(self.min_wait_time,self.max_wait_time))

		else:#and there every messgae is a single request
			sent = 0
			while sent < len(ids):
				r.append(self.msg(msg, ids[sent]))
				while type(r[sent]) is list and r[sent][0] == 'captcha':
					r[sent]=self.enter_captcha(r[sent][1].get('captcha_img'), r[sent], [['message', msg]])
				if r[sent] is list:
					print(r[sent][0])
				else:
					print('sent')
					sent+=1
				sleep(randint(self.min_wait_time,self.max_wait_time))

		return r






	def comment_spammer(self, ids, messages, attachments = [], offset = 11):#TODO: jsoner
			for i in ids:#each group
				last_posts = get_last_posts(i, 1, offset)
				for j in range(0, len(last_posts)):#each post
					for message_number in range(0, len(messages)):#if 2 or more comments on each post
						try:
							if last_posts[j] == None:
								print('error')
								continue
							r=comment(int(i), int(last_posts[0].get('items')[j].get('id')), messages[message_number], attachments[message_number]).json()#request
							print('nice, comment id: ' + str(r.get('response').get('comment_id')) + ', it is ' + str(j) + ' in group ' + i)#debug
						except BaseException:
							continue

						sleep(randint(self.time_for_wait_min, self.time_for_wait_max))





	def add_friends(self, ids, msg = 'Привет, где-то тебя видел. На всякий случай добавь в друзья.)'):
		
		friends_added = 0
		i = 0

		while friends_added < len(ids):
			print(1)
			r = self.add_friend(ids, msg)#TODO: use offset
			while type(r) is list and r[0] == 'captcha': r = self.enter_captcha(r[1].get('captcha_img'), r)
			if r == 1 or r == 4: friends_added+=1#codes where this shit actually goes out

			i+=1
			if(r ==1): print('trying to add, total:  ' + str(friends_added))
			elif(r==2): print('already added, total:  ' + str(friends_added))
			elif(r==4): print('sending again, total: ' + str(friends_added))
			sleep(randint(self.min_wait_time, self.max_wait_time))





	def enter_captcha(self, url, r, additional=[]):#TODO: use tk.py file, app class.
		pic = req.get(url, stream = True)
		with open('captcha.jpg', 'wb') as fd:
			for chunk in pic.iter_content(chunk_size=128):#TODO: write at var directly, not via saving it to file.
				print(chunk)
				fd.write(chunk)#saving capthca picture to file

		def captcha_sender(r, captcha_key):#TODO: fix ЏРєРёР symbols.
			resp=r[1]
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