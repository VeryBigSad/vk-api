from collections import namedtuple

from flask import Flask, render_template

app = Flask('test')

Bot = namedtuple('token', 'type')
bots = []


@app.route('/')
def main():
    return render_template('index.html')
    # return 'helloworld'


@app.route('/main', methods=['GET'])
def asd():
    return render_template('asd.html')


@app.route('/add_bot', methods=['POST'])
def add_bot():
    return 1


