# -*- coding: utf-8 -*-

############################################################################################################################################################################################################
###########################################                               HERE COMES THE VK API CALLBACK SHIT, OH YEAAAAAAAAAAAAAH                               ###########################################
############################################################################################################################################################################################################
from flask import Flask, request, json


app = Flask('mrb')
confrimation_token = 'e38e3fd0'

@app.route('/')
def go_away():
	return 'go away you dirty pig'

@app.route('/', methods=['POST'])
def router():
	data = json.loads(request.data)
	print(data)
	return confrimation_token