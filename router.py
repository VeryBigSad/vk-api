import group_bot
from flask import *

app = Flask('mrb')
confrimation_token = 'e38e3fd0'


type = 'test'


@app.route('/', methods=['POST'])
def router():
	return confrimation_token



app.run(host="0.0.0.0", port="80")
#просто убрать когда понадобится импортить файл

