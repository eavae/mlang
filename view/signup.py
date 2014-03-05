#coding:utf-8
from view import app
from flask import request,redirect,jsonify
from model.user import User,UserDetail
from model.tools import validate_email,pack_password,vali_nickname,langName
from flask_login import login_user,current_user,login_required
from flask.ext.babel import gettext as _
from flask.ext.babel import refresh
from view.util.render import render

def signup_base():
    errors = {}
    try:
        email = request.form['email']
        password = request.form['password']
        try:
            confirm = request.form['confirm']
        except KeyError:
            confirm = password
        if not password == confirm:
            errors['password'] = _(u"Inconsistent password twice.")
        if not validate_email(email):
            errors['email'] = _(u"please check your email address again")
        if len(password) < 6:
            errors['password'] = _(u"Your password is too short. At least 6 characters.")
    except KeyError:
        errors['KeyError'] = _(u'key error')

    if not errors:
        user = User.query.filter_by(email=email).first()
        if user:
            errors['email'] = _(u'this email has been used')
        else:
            user = User(email,pack_password(password))
            user.commit()
            detail = UserDetail(user)
            detail.commit()
            login_user(user)
            refresh()
    return errors

def required_base():
    errors = {}
    try:
        nickname = request.form['nickname']
        native = request.form['native']
        learning = request.form['learning']
        if not vali_nickname(nickname):
            errors['nickname'] = _(u"Please enter the correct nickname, nickname must has 1-40 characters")
        if not langName(native):
            errors['native'] = _(u"Language error, system don't support this language")
        if not langName(learning):
            errors['learning'] = _(u"Language error, system don't support this language")
    except KeyError:
        errors['KeyError'] = _(u"key error")
    if not errors:
            current_user.nickname = nickname
            current_user.native = native
            current_user.learning = learning
            current_user.commit()
    return errors

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    errors = {}
    if request.method == 'POST':
        errors = signup_base()
        if not errors:
            return redirect("/required")
    return render('signup.html', errors = errors)

@app.route('/j/signup', methods=['POST'])
def j_signup():
    errors = signup_base()
    data = {}
    result = {}
    if not errors:
        data['state'] = 'OK'
        data['uid'] = current_user.id
    result['errors'] = errors
    result['data'] = data
    return jsonify(result)

@app.route('/required', methods=['POST', 'GET'])
@login_required
def required():
    errors = {}
    if request.method == 'POST':
        errors = required_base()
        if not errors:
            return redirect('/t/')
    return render('required.html',errors = errors)

@app.route('/j/required',methods=['POST'])
@login_required
def j_required():
    data,result = {}
    errors = required_base()
    if not errors:
        data['state'] = "OK"
        result['data'] = data
        return jsonify(result)
    else:
        result['errors'] = errors
        return jsonify(result)