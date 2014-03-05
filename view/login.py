from view import app
from flask import request,redirect,jsonify
from flask.ext.babel import gettext as _
from model.tools import validate_email,pack_password
from model.user import User
from flask_login import login_user,current_user,logout_user
from view.util.render import render

@app.route('/login',methods=['GET','POST'])
def login():
    errors ={}
    next = request.args.get('next', '/')
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            next = request.form['next']
            try:
                rememberme = request.form['rememberme']
            except KeyError:
                rememberme = False
            if not validate_email(email):
                errors['email'] = _(u"please check your email address again")
        except KeyError:
            errors['KeyError'] = _(u"key error")

        if not errors:
            user = User.getByEmail(email)
            if user:
                if pack_password(password) == user.password:
                    login_user(user,remember=rememberme)
                    if (not user.nickname) or (not user.learning) or (not user.native):
                        return redirect('/required')
                    else:
                        return redirect(next)
                else:
                    errors['password'] = _(u"password error, please enter again.")
            else:
                errors['email'] = _(u"this email doesn't exist.")
    return render('login.html', errors = errors, next = next)

@app.route('/j/login',methods=['POST'])
def j_login():
    errors={}
    data={}
    try:
        email = request.form['email']
        password = request.form['password']
        if not validate_email(email):
            errors['email'] = _(u"please check your email address again")
    except KeyError:
        errors['KeyError'] = _(u"key error")
    if not errors:
        user = User.getByEmail(email)
        if user:
            if pack_password(password) == user.password:
                login_user(user,remember=True)
                data['email'] = email
                data['uid'] = user.id
                data['nickname'] = user.nickname
                data['native'] = user.native
                data['learning'] = user.learning
                data['state'] = 'OK'
            else:
                errors['password'] = _(u"password error, please enter again.")
        else:
            errors['email'] = _(u"this email doesn't exist.")
    result = {}
    result['errors'] = errors
    result['data'] = data
    return jsonify(result)

@app.route('/j/islogin',methods=['GET'])
def j_islogin():
    result,data = {},{}
    if not current_user.is_anonymous():
        data['email'] = current_user.email
        data['uid'] = current_user.id
        data['nickname'] = current_user.nickname
    else:
        result['errors'] = _(u"Not login.")
    result['data'] = data
    return jsonify(result)


@app.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect('/')
