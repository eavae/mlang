#coding:utf-8
from view import app,avatar
from flask_login import login_required,current_user
from flask import request,jsonify,redirect,flash
from flask.ext.babel import gettext as _
from model.tools import langName
from model.user import UserDetail
from model.twitter import Twitter
from model.tcomment import TComment
from model.tamend import TAmend
from model.acomment import AComment
from view.util.render import render
from bs4 import BeautifulSoup
import json

def convert_btn_to_a(string):
    soup = BeautifulSoup(string)
    buttons = soup.findAll('button')
    for button in buttons:
        info = button['name'].replace('@','').replace('\'','\"')
        info = json.loads(info)
        a = soup.new_tag("a")
        a['href'] = '/user/'+info['uid']
        a.string = info['nick']
        button.replace_with(a)
    if buttons:
        result = _(u"Reply to ") + unicode(soup)
        pos = result.find('</a>')+4
        result = result[:pos] + ' : ' + result[pos:]
    else:
        result = unicode(soup)
    return result

def twitter_new_base():
    errors = {}
    try:
        content = request.form['content']
        language = request.form['language']
        if len(content) > app.config['TEXT_MAX_LENGTH']:
            errors['content'] = _(u"Content is too long.")
        if not langName(language):
            errors['language'] = _(u"Language error, system don't support this language")
    except KeyError:
        errors['KeyError'] = _(u"key error")
    if not errors:
        t = Twitter(current_user,content,language)
        t.commit()
    return errors

def t_index_base(lang):
    twitters = Twitter.getAll(lang=lang)
    results = []
    for twitter in twitters:
        t = twitter.getDict()
        t['timedelta'] += _(u" ago")
        t['nickname'] = twitter.user.nickname
        t['purpose'] = UserDetail.getById(twitter.user.id).purpose if UserDetail.getById(twitter.user.id) else ''
        t['amends'] = twitter.amends.count()
        t['comments'] = twitter.comments.count()
        results.append(t)
    return results
    
@app.route('/t/new',methods=['POST'])
@login_required
def twitter_new():
    errors = twitter_new_base()
    for key,value in errors.items():
        flash(value,'danger')
    if not errors:
        flash(_("Post text successfully!"),'success')
    return redirect('/t')

@app.route('/j/t/new',methods=['POST'])
@login_required
def j_twitter_new():
    errors = twitter_new_base()
    data,result = {}
    if not errors:
        data['state'] = 'OK'
    result['errors'] = errors
    result['data'] = data
    return jsonify(result)

@app.route('/t/',methods=['GET'])
def t_index():
    if current_user.is_anonymous:
        lang = request.args.get('lang','en')
    else:
        lang = request.args.get('lang',current_user.learning)
    if not langName(lang):
        lang = 'en'
    results = t_index_base(lang)
    return render('t/index.html',results = results, language=lang, avatar=avatar)

@app.route('/j/t/',methods=['GET'])
def j_t_index():
    if current_user.is_anonymous:
        lang = request.args.get('lang','en')
    else:
        lang = request.args.get('lang',current_user.learning)
    if not langName(lang):
        lang = 'en'
    return jsonify(t_index_base(lang))

def t_amend_base():
    errors = {}
    try:
        tid = request.form['tid']
        amend = request.form['amend']
        explain = request.form['explain']
        twitter = Twitter.getById(tid)
        if len(amend) > app.config['TEXT_MAX_LENGTH']:
            errors['amend'] = _(u"Amend is too long.")
        if len(explain) > app.config['TEXT_MAX_LENGTH']:
            errors['explain'] = _(u"Explain is too long.")
        if not twitter:
            errors['tid'] = _(u"This twitter doesn't exist.")
    except KeyError:
        errors['KeyError'] = _(u"key error")

    if not errors:
        tamend = TAmend(current_user,twitter,amend,explain)
        tamend.commit()
    return errors

@app.route('/t/amend',methods=['POST'])
@login_required
def t_amend():
    errors = t_amend_base()
    for key,value in errors.items():
        flash(value,'danger')
    if not errors:
        tid = request.form['tid']
        flash(_("Post amend successfully!"),'success')
    return redirect('/t/detail/'+tid)

@app.route('/j/t/amend',methods=['POST'])
@login_required
def j_t_amend():
    data,results = {},{},{}
    errors = t_amend_base()
    if not errors:
        data['state'] = 'OK'
    results['errors'] = errors
    results['data'] = data
    return jsonify(results)

def t_detail_base(tid):
    twitter = Twitter.getById(tid)
    results = twitter.getDict()
    results['timedelta'] += _(u" ago")
    results['nickname'] = twitter.user.nickname
    results['purpose'] = UserDetail.getById(twitter.user.id).purpose if UserDetail.getById(twitter.user.id) else ''
    results['comments'] = []
    for comment in twitter.comments:
        c = comment.getDict()
        c['timedelta'] += _(u" ago")
        c['nickname'] = comment.user.nickname
        c['purpose'] = UserDetail.getById(comment.user.id).purpose if UserDetail.getById(comment.user.id) else ''
        results['comments'].append(c)
    results['amends'] = []
    for amend in twitter.amends:
        a = amend.getDict()
        a['timedelta'] += _(u" ago")
        a['nickname'] = amend.user.nickname
        a['purpose'] = UserDetail.getById(amend.user.id).purpose if UserDetail.getById(amend.user.id) else ''
        a['comments'] = []
        for comment in amend.comments:
            c = comment.getDict()
            c['timedelta'] += _(u" ago")
            c['nickname'] = comment.user.nickname
            c['purpose'] = UserDetail.getById(comment.user.id).purpose if UserDetail.getById(comment.user.id) else ''
            a['comments'].append(c)
        results['amends'].append(a)
    return results

@app.route('/t/detail/<int:tid>',methods=['GET'])
def t_detail(tid):
    results = t_detail_base(tid)
    return render('t/detail.html',twitter=results,avatar=avatar)

@app.route('/j/t/detail/<int:tid>',methods=['GET'])
def j_t_detail(tid):
    results = t_detail_base(tid)
    return jsonify(results)

def t_comment_base():
    errors = {}
    try:
        twitter_id = request.form['tid']
        comment = request.form['comment']
        twitter = Twitter.getById(twitter_id)
        if not twitter:
            errors['twitter'] = _(u"This twitter doesn't exit.")
        if len(comment) > app.config['TEXT_MAX_LENGTH']:
            errors['comment'] = _(u"Comment is too long.")
    except KeyError:
        errors['KeyError'] = _(u"key error")

    if not errors:
        comment = convert_btn_to_a(comment)
        tc = TComment(current_user,twitter,comment)
        tc.commit()
    return errors

@app.route('/t/comment',methods=['POST'])
@login_required
def t_comment():
    errors = t_comment_base()
    for key,value in errors.items():
        flash(value,'danger')
    if not errors:
        flash(_("Post reply successfully!"),'success')
        tid = request.form['tid']
    return redirect('/t/detail/'+tid)

@app.route('/j/t/comment',methods=['POST'])
@login_required
def j_t_comment():
    data,results = {},{}
    errors = t_comment_base()
    if not errors:
        data['state'] = 'OK'
    results['errors'] = errors
    results['data'] = data
    return jsonify(results)

def t_acomment_base():
    errors = {}
    try:
        amend_id = request.form['aid']
        comment = request.form['comment']
        print comment
        amend = TAmend.getById(amend_id)
        if not amend:
            errors['amend'] = _(u"This amend doesn't exist.")
        if len(comment) > app.config['TEXT_MAX_LENGTH']:
            errors['comment'] = _(u"Comment is too long.")
    except KeyError:
        errors['KeyError'] = _(u"key error")
    if not errors:
        comment = convert_btn_to_a(comment)
        ac = AComment(current_user,amend,comment)
        ac.commit()
    return errors
#acomment is the amend's comment
@app.route('/t/acomment',methods=['POST'])
@login_required
def t_acomment():
    errors = t_acomment_base()
    for key,value in errors.items():
        flash(value,'danger')
    if not errors:
        flash(_("Post reply successfully!"),'success')
        tid = request.form['tid']
    return redirect('/t/detail/'+tid)

@app.route('/j/t/acomment',methods=['POST'])
@login_required
def j_t_acomment():
    data,results = {},{}
    errors = t_acomment_base()
    if not errors:
        data['state'] = 'OK'
    results['errors'] = errors
    results['data'] = data
    return jsonify(results)