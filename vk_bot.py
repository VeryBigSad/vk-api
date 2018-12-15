# -*- coding: utf-8 -*-
from vk import *

import Tkinter as tk#do this shit in main.py
from PIL import Image, ImageTk


class bot(vk):
	def __init__(self, token, min_wait_time=3, max_wait_time=6, api_version=5.90):
		vk.__init__(self, token, min_wait_time, max_wait_time, api_version)
		self.id = self.method('users.get', {}).json().get('response')[0].get('id')


	def msg_spammer(self, msg, count, ids=None):
		if ids == None:
			ids = self.get_rand_ids(count)
		r=[]
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





	def add_friends(self, count, ids=None, msg = 'Привет, где-то тебя видел. На всякий случай добавь в друзья.)'):
		#TODO: по какой-то причине зависает после выполнения, почему?
		friends_added = 0
		i = 0
		if ids == None:
			ids = self.get_rand_ids(count)

		while friends_added < len(ids):
			r = self.add_friend(ids, msg)#TODO: use offset
			while type(r) is list and r[0] == 'captcha': r = self.enter_captcha(r[1].get('captcha_img'), r)
			if r == 1 or r == 4: friends_added+=1#codes where this shit actually goes out

			if(r ==1): print('trying to add, total:  ' + str(friends_added))
			elif(r==2): print('already added, total:  ' + str(friends_added))
			elif(r==4): print('sending again, total: ' + str(friends_added))
			sleep(randint(self.min_wait_time, self.max_wait_time))





