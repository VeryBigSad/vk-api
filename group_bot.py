# -*- coding: utf-8 -*-

from flask import Flask, request, json
from sys import path
from vk import *

class group(vk):

	def mass_ban(self, ids):
		for id in ids:
			self.group_ban(id, self.id, )





	