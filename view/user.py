#coding:utf-8
from view import app,avatar
from flask_login import login_required,current_user
from flask import abort,request
from flask.ext.babel import gettext as _
from model.user import User,UserDetail
from model.twitter import Twitter
from view.util.render import render
from model.const import I18n
from datetime import datetime


@app.route('/user/<int:uid>/',methods=['GET'])
def user_uid_index(uid):
    user = User.getById(uid)
    twitters = Twitter.getByUser(user)
    results = []
    for twitter in twitters:
        t = twitter.getDict()
        t['timedelta'] += _(u"ago")
        t['amends'] = twitter.amends.count()
        t['comments'] = twitter.comments.count()
        results.append(t)
    return render('user/index.html',twitters=results,uid=uid)

@app.route('/user/<int:uid>/info',methods=['GET'])
@login_required
def user_uid_info(uid):
    if current_user.is_anonymous() or current_user.id != uid:
        abort(403)
    return render('user/info.html',
        uid=uid,
        detail=UserDetail.getById(current_user.id),
        avatar_urls=(avatar.getAvatarUrl(current_user.id,'s'),
            avatar.getAvatarUrl(current_user.id,'m'),
            avatar.getAvatarUrl(current_user.id,'l')),
        userinfo=current_user.getDict())

def setting_post_base():
    user = current_user
    detail = UserDetail.getById(user.id)
    f = request.form
    user.nickname = f.get('nickname',user.nickname)
    user.native = f.get('native',user.native)
    user.learning = f.get('learning',user.learning)
    user.locale = f.get('locale',user.locale)
    avatarfile = request.files['avatar']
    if avatarfile:
        avatar.saveAvatar(avatarfile,user.id)
    detail.realname = f.get('realname',detail.realname)
    if f.get('birth',detail.birth.isoformat()):
        detail.birth = datetime.strptime(f.get('birth',''), "%Y-%m-%d")
    detail.gender = f.get('gender',detail.gender)
    detail.job = f.get('job',detail.gender)
    detail.purpose = f.get('purpose',detail.purpose)
    detail.presentation = f.get('presentation',detail.presentation)
    user.commit()
    detail.commit()
    pass

@app.route('/user/<int:uid>/setting',methods=['GET','POST'])
@login_required
def user_uid_setting(uid):
    if current_user.is_anonymous() or current_user.id != uid:
        abort(403)
    if request.method == 'POST':
        setting_post_base()
    return render('user/setting.html',
        uid=uid,langs=I18n.LANG,
        locales=I18n.LOCALE,
        detail=UserDetail.getById(current_user.id))