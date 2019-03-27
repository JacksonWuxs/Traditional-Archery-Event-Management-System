from flask_login import (current_user, login_required,
                         login_user, logout_user)
from cPickle import dump, load
from .session import User
from .db import database


HomeDB = database('db/home.db')

def register(user, email, psd):
    # Check register info
    taken_email = HomeDB.select('Email = "%s"' % email)
    if len(taken_email) != 0:
        return render_template('register.html', type='ERROR', errors='Your email has been taken, try to reset the password.')

    # Temporay save register info
    confirm_code = md5(email + str(clock())).hexdigest()
    info = dict(user=user, email=email, psd=psd)
    dump(info, open('temporary/home/%s.pkl' % confirm_code, 'wb'))

    # Send confirm email
    msg = Message("[Kitgram] Confirm E-mail", sender='JW_Library@163.com', recipients=[email, ])
    msg.body = '\n'.join([
        "Welcome %s!\n" % user,
        "Thanks for signing up with Jackson Woo's Library!",
        'You must follow this link to activate your account:',
        'http://www.kitgram.cn/register/confirm/%s \n' % confirm_code,
        'If this is not your action behavior, please ignore the message, sorry.'])
    send_async_email(app, msg, mail)
    return render_template('register.html', type='INFO', errors='We have sent a confirm mail to you. Please check your email.')

def confirm(code):
    info = load(open('temporary/register/%s.pkl' % code))
    HomeDB.add_user('NULL', info['user'], info['psd'], info['email'])
    remove('temporary/register/%s.pkl' % code)
    user = User(email=info['email'])
    login_user(user, remember=False)
    return redirect('/')

def login(email, psd):
    user = User(email)
    if user._mode == 'guest':
        return render_template('login.html', type='ERROR', errors='Invalid user account!')
    if not user.verify_password(psd):
        return render_template('login.html', type='ERROR', errors='Incorrect password!')
    login_user(user, remember=True)
    return redirect('/')
