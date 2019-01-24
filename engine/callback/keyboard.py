# -*- coding: utf-8 -*-
#здесь будет всяко-разная дичь по работе с клавой

class keyboard:
	def __init__(self, rows, columns, is_one_time, ):
		self.rows = rows
		self.columns = columns

	def add_collumn(self):
		self.collumn = self.columns+1
	def add_row(self):
		self.rows = self.rows+1
	def delete_keyboard(self):

