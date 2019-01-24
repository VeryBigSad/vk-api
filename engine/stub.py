from flask import *
import json

vk = Flask('vk')
@vk.route('/', methods=['POST'])
def handler():
	a = json.dumps({'error': {'error_code': 'stub', 'request_params':[{'key': 'method', 'value':'stub.stub'}, {'key': 'v', 'value': '5.92'}]}})
	print(json.loads(a))
	return a
vk.run(host="0.0.0.0", port="22824")
