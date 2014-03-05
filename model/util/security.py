# -*- coding: utf-8 -*- 
import datetime
import urllib

from google.appengine.ext import ndb
from google.appengine.api import memcache

from model.l10n import GetMessages
from model.util.cookies import Cookies
from model.db import Member

#在memcache中缓存auth=>member_id,Member_mid=>member

def GetIP(handler):
    if 'X-Real-IP' in handler.request.headers:
        return handler.request.headers['X-Real-IP']
    else:
        return handler.request.remote_addr

def CheckAuth(handler):
    ip = GetIP(handler)
    cookies = handler.request.cookies
    if 'auth' in cookies:
        auth = cookies['auth']
        member_id = memcache.get(auth)
        if member_id:
            member = memcache.get('Member_'+str(member_id))
            if member is None:
                member = Member.get_by_id(int(member_id))
                if member:
                    memcache.set(auth, member.key.id())
                    memcache.set('Member_' + str(member.key.id()), member)
                else:
                    member = False
            if member:
                member.ip = ip
            return member
        else:
            q_members = Member.query(Member.auth == auth)
            if q_members.count() == 1:
                member = q_members.get()
                member_id = member.key.id()
                memcache.set(auth, member_id)
                memcache.set('Member_'+str(member_id), member)
                member.ip = ip
                return member
            else:
                return False
    else:
        return False

def SetAuth(handler, member):
    memcache.set(member.auth, member.key.id())
    cookie_string = 'auth=%s; expires=%s; path=/'%(member.auth, (datetime.datetime.now() + datetime.timedelta(days=365)).strftime("%a, %d-%b-%Y %H:%M:%S GMT"))
    handler.response.headers['Set-Cookie'] = str(cookie_string)

def UnsetAuth(handler):
    cookies = Cookies(handler, max_age = 86400, path = '/')
    del cookies['auth']

def member_required(handler):
    from model.util.common import GetSite
    member = CheckAuth(handler)
    if member:
        return member
    else:
        # TODO::need login message
        l10n = GetMessages(False, GetSite())
        handler.redirect('/signin?redirect_url='+(handler.request.url))
