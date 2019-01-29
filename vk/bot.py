# -*- coding: utf-8 -*-
from engine.vk import *

# import Tkinter as tk  # do this shit in main.py
# from PIL import Image, ImageTk


class bot(vk):
	def __init__(self, token, testing_mode=False,logger_name='vk', log_level='info',min_wait_time=3, max_wait_time=6, api_version=5.90):
		vk.__init__(self, token, testing_mode,min_wait_time, max_wait_time,logger_name,log_level, api_version)

		self.id = self.get_usrinfo()
		self.log.debug('id of bot is ' +str(self.id))
		self.log.info('Bot class started!\n')



	def msg_spammer(self, msg, count, ids=None):#working
		if ids == None:
			ids = self.get_rand_ids(count)
		r=[]
		sent = 0
		while sent < len(ids):
			r.append(self.msg(msg, ids[sent]))
			#while type(r[sent]) is list and r[sent][0] == 'captcha': r[sent]=self.enter_captcha(r[sent][1].get('captcha_img'), r[sent], [['message', msg]])
			if r[sent] is list:
				self.log.debug(r[sent][0])
			else:
				self.log.debug('sent')
				sent+=1
			sleep(randint(self.min_wait_time,self.max_wait_time))

		return r






	def comment_spammer(self, group_ids, messages, posts_per_group=5, attachment='', offset = 1):#working
		self.log.info('starting comment_spammer()...')
		comments_sent=0
		for i in group_ids:#each group
			last_posts = self.get_last_posts(i, posts_per_group, offset)
			if len(last_posts) - posts_per_group < 0: self.log.warning('group or user '+str(i)+' not valid, not enough posts. skipping him.');continue
			
			for j in range(0, len(last_posts)):#each post
				if type(messages) is list:   r=self.jsoner(self.comment(int(i), int(last_posts[j].get('id')), messages[message_number], attachments[message_number]))#request
				else:                        r=self.jsoner(self.comment(int(i), int(last_posts[j].get('id')), messages, attachment))#request
				if r.get('error_code') != None:
					self.log.error('comment didn\'t gone, reason(if its num contact author): '+r.get('error_code'))
					# if r.get('error_code') == 'capthca': self.enter_captcha()
					# TODO: not only this, but also put all in the while cycle
					sleep(randint(self.min_wait_time, self.max_wait_time))
					continue
				comments_sent+=1
				self.log.info('comment sent, total: ' +str(comments_sent))
				sleep(randint(self.min_wait_time, self.max_wait_time))
			self.log.info
		self.log.info('comment_spammer() finished, totally sent '+str(comments_sent)+' comments\n\n')




	def add_friends(self, count, ids=None, msg = 'Привет, где-то тебя видел. На всякий случай добавь в друзья.)'):
		#TODO: по какой-то причине зависает после выполнения, почему?
		friends_added = 0
		i = 0
		if ids == None: ids = self.get_rand_ids(count)

		while friends_added < len(ids):
			r = self.add_friend(ids, msg)#TODO: use offset
			#while type(r) is list and r[0] == 'captcha': r = self.enter_captcha(r[1].get('captcha_img'), r)
			if r == 1 or r == 4: friends_added+=1#codes where this shit actually goes out

			if(r ==1): self.log.info('trying to add, total:  ' + str(friends_added))
			elif(r==2): self.log.info('already added, total:  ' + str(friends_added))
			elif(r==4): self.log.info('sending again, total: ' + str(friends_added))
			sleep(randint(self.min_wait_time, self.max_wait_time))



