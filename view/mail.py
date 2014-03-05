#coding:utf-8
import pylibmc
import uuid
from view import app
from flask import render_template,redirect,request
from flask_login import current_user,login_user
from flask.ext.babel import gettext as _
from model.tools import QQMail
from model.user import User
from functools import wraps

def user_check(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        #user not logged in
        if current_user.is_anonymous():
            return redirect('/login')
        #user is authed, don't need again
        elif current_user.is_auth:
            return render_template('email/authed.html')
        else:
            return func(*args, **kwargs)
    return decorated_view

@app.route('/email/send',methods=['GET'])
@user_check
def email_send():
    mc = pylibmc.Client()
    token = mc.get(str(current_user.id)+'uuid')
    if token:
        info = _(u"Please check your email inbox to verify the e-mail address")
    else:
        token = uuid.uuid4()
        mc.set(str(current_user.id)+'uuid',token,app.config['MAILUUID_EXIST_TIME'])
        m = QQMail(app.config['QQMAIL_ACCOUNT'],app.config['QQMAIL_PASSWORD'])
        title = _(u"MLang -- email verify")
        content = render_template('email/to_user.html',host=app.config['HOST_URL'],uid=current_user.id,token=token)
        m.send(current_user.email,title,content)
        info = _(u"Verify email has send to your email inbox, Please check it.")
    return render_template('email/send.html',info=info)

@app.route('/email/resend',methods=['GET'])
@user_check
def email_resend():
    mc = pylibmc.Client()
    token = uuid.uuid4()
    mc.set(str(current_user.id)+'uuid',token,app.config['MAILUUID_EXIST_TIME'])
    m = QQMail(app.config['QQMAIL_ACCOUNT'],app.config['QQMAIL_PASSWORD'])
    title = _(u"MLang -- email verify")
    content = render_template('email/to_user.html',host=app.config['HOST_URL'],uid=current_user.id,token=token)
    m.send(current_user.email,title,content)
    info = _(u"Verify email has resend to your email inbox, Please check it.")
    return render_template('email/send.html',info = info)

@app.route('/email/check',methods=['GET'])
def email_check():
    errors = {}
    uid = request.args.get('uid','')
    token = request.args.get('token','')
    mc = pylibmc.Client()
    utoken = mc.get(str(uid)+'uuid')
    if str(utoken) == str(token):
        user = User.getById(uid)
        print "hello"
        if user:
            user.is_auth = True
            user.commit()
            login_user(user)
        else:
            errors['user'] = _(u"This user doesn't exist")
    else:
        errors['token'] = _(u"The token is error, Please try to resend email to verify email.")
    return render_template("email/result.html",errors = errors)