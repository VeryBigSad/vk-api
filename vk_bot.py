# -*- coding: utf-8 -*-
from vk import *

import Tkinter as tk#do this shit in main.py
from PIL import Image, ImageTk


class bot(vk):

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