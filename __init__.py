from flask import Flask, render_template, redirect, request

import site.info_templates

app = Flask('app')

# accounts = [{'login': 'admin', 'password': '12345'}]


@app.route('/', methods=['POST', 'GET'])
def home():
    info_template['title'] = 'Main Page'
    return render('index.html', info_template)


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/u/<userlogin>')
def cabinet(userlogin):
    render_template('cabinet.html', user=get_usr_info(userlogin))


@app.route('/signin')
def signin():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def loginmachine():
    type = request.type
    login = request.login
    password = request.password

    if type == 'login' and accounts.index({'login': login, 'password': password}):
        return redirect('/u/' + login)
    if type == 'register':
        accounts.append({'login': login, 'password': password})
        return redirect('/u/' + login)


# @app.route('/add_bot', methods=['POST'])
# def add_bot():
#     return render_template('add_bot.html')
