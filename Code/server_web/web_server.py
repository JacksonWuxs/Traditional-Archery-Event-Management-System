#!/usr/bin/python
# -*- coding: utf-8 -*-

from md5 import md5
from os import path, remove
from random import randint
from flask import (Flask, abort, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from flask_login import LoginManager
from tk.home_server import register, confirm, login
from datetime import datetime

HOST = '0.0.0.0'
PORT = 80
DEBUG = True

app = Flask(__name__)
app.config.from_pyfile(r'tk/config.cfg')

login_manager = LoginManager(app)
login_manager.seesion_protection = 'strong'
login_manager.login_view = 'login'

def auto_abort(func):
    def wrapper(*arg, **func):
        try:
            return func(*arg, **func)
        except IOError:
            abort(404)
        except Exception as e:
            abort(500)
    return wrapper

@auto_abort
@app.route('/', methods=['GET', 'POST'])
def page_home():
    r = request.url[7:].split('.')[0].lower()
    if r not in ('dapy', 'taems', 'ucac'):
        return render_template('home.html')
    return render_template(r + '.html')

@auto_abort
@app.route('/chatbot', methods=['get'])
def page_chatbot():
    return render_template('chat_home.html')

@auto_abort
@app.route('/ucac/register', methods=['get'])
def page_ucac_register():
    return render_template('ucac_register.html')

@auto_abort
@app.route('/ucac/score', methods=['get'])
def page_ucac_score():
    return redirect('http://www.kitgram.cn:5000/ucac/score')

@auto_abort
@app.route('/ucac/register', methods=['POST'])
def do_register():
    user = request.form['name'].encode('utf-8')
    email = request.form['email'].encode('utf-8')
    psd = md5(request.form['password'].encode('utf-8')).hexdigest()
    return register(user, email, psd)

@app.route('/404', methods=['GET', 'POST'])
def page_404():
    try:
        return render_template('404.html')
    except IOError:
        return 'Page not found', 404
    except Exception as e:
        abort(500)

@app.errorhandler(404)
def do_not_found(e):
   return redirect('404')

@auto_abort
@app.route('/Library/<dirname>/<filename>', methods=['GET'])
def do_download(dirname, filename):
    addr = path.join('downloads', dirname)
    response = send_from_directory(addr, filename, as_attachment=True)
    response.headers['Content-Disposition'] = 'attachment;filename=%s' % filename
    return response

@auto_abort
@app.route('/register', methods=['GET'])
def page_register():
    return render_template('register.html', type='')

@auto_abort
@app.route('/register/confirm/<code>', methods=['Get'])
def page_confirm(code):
    if path.isfile('temporary/register/%s.pkl' % code) is False:
        raise IOError
    return confirm(code, User)

@auto_abort
@app.route('/login', methods=['Get'])
def page_login():
    return render_template('login.html')

@auto_abort
@app.route('/login', methods=['POST'])
def do_login():
    email = request.form['email'].encode('utf-8')
    psd = md5(request.form['password'].encode('utf-8')).hexdigest()
    return login(email, psd)

@auto_abort
@app.route('/user/<username>', methods=['GET'])
def manage():
    abort(404)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
