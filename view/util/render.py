#coding:utf-8
from flask import render_template
from flask_login import current_user

def render(uri,*args, **kwds):
    return render_template(uri,user=current_user,*args,**kwds)