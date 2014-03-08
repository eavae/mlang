# -*- coding: utf-8 -*- 

import datetime
import hashlib

from google.appengine.ext import ndb
from google.appengine.api import memcache

from babel.dates import format_date,format_timedelta,get_timezone

def time_localed(time, member):
    delta = time - datetime.datetime.now()
    if member:
        locale = member.native_lang
    else:
        locale = 'en'
    return format_timedelta(delta, locale=locale)

class Member(ndb.Model):
    auth = ndb.StringProperty(required=True, indexed=True)
    deactivated = ndb.BooleanProperty(required=True, default=False)
    username = ndb.StringProperty(indexed=True)
    username_lower = ndb.ComputedProperty(lambda self: self.username.lower(), indexed=True)
    password = ndb.StringProperty(required=True, indexed=True)
    email = ndb.StringProperty(required=True, indexed=True)
    email_verified = ndb.BooleanProperty(indexed=True, default=False)
    website = ndb.StringProperty(default='')
    favorite_lang = ndb.StringProperty(default='')
    native_lang = ndb.StringProperty(default='')
    location = ndb.StringProperty(default='')
    avatar = ndb.StringProperty()
    created_time = ndb.DateTimeProperty(auto_now_add=True)
    updated_time = ndb.DateTimeProperty(auto_now=True)
    last_signin_time = ndb.DateTimeProperty()
    l10n = ndb.StringProperty(default='zh_CN')
    notifications = ndb.IntegerProperty(required=True, default=0)
    notification_position = ndb.IntegerProperty(required=True, default=0)
    private_token = ndb.StringProperty(indexed=True)
    motto = ndb.TextProperty(default='')
    introduce = ndb.TextProperty(default='')

    @property
    def username_lower_md5(self):
        return hashlib.md5(self.username_lower).hexdigest()

    @property
    def created_timestamp(self):
        return self.created_time.strftime("%s")

    def _pre_put_hook(self):
        memcache.set(self.auth, str(self.key.id()))
        memcache.set('Member_'+str(str(self.key.id())), self)


class Counter(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    value = ndb.IntegerProperty(default=0)
    created_time = ndb.DateTimeProperty(auto_now_add=True)
    updated_time = ndb.DateTimeProperty(auto_now=True)

class Section(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    created_time = ndb.DateTimeProperty(auto_now_add=True)
    updated_time = ndb.DateTimeProperty(auto_now=True)
"""
Node 为根据语种分类的节点
"""
class Node(ndb.Model):
    section_key = ndb.KeyProperty(indexed=True)
    name = ndb.StringProperty(indexed=True)
    title = ndb.StringProperty(indexed=True)
    created_time = ndb.DateTimeProperty(auto_now_add=True)
    updated_time = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def getsBySection(cls, section):
        nodes = []
        #check each section has 3 node
        q = cls.query(cls.section_key==section.key)
        if q.count() == 0:
            print "Create nodes for "+section.name
            node_en = Node(name='en', title='english', section_key=section.key)
            node_zh_CN = Node(name='zh_CN', title='simple chinese', section_key=section.key)
            node_ja = Node(name='ja', title='japnese', section_key=section.key)
            node_en.put()
            node_zh_CN.put()
            node_ja.put()
            nodes.append(node_ja)
            nodes.append(node_en)
            nodes.append(node_zh_CN)
        else:
            for result in q:
                nodes.append(result)
        return nodes

#用户所发表的文章片段
class Topic(ndb.Model):
    node_key = ndb.KeyProperty(kind=Node)
    member_key = ndb.KeyProperty(kind=Member)
    title = ndb.StringProperty(indexed=True)
    has_content = ndb.BooleanProperty(required=True, default=True)
    content = ndb.TextProperty()
    content_length = ndb.IntegerProperty(required=True, default=0)
    hits = ndb.IntegerProperty(default=0)
    votes = ndb.IntegerProperty(required=True, default=0)
    replies = ndb.IntegerProperty(default=0)
    amends = ndb.IntegerProperty(default=0)
    last_reply_by = ndb.KeyProperty(kind=Member)
    explicit = ndb.IntegerProperty(required=True, default=0)
    created_time = ndb.DateTimeProperty(auto_now_add=True)
    updated_time = ndb.DateTimeProperty(auto_now=True)
    touched_time = ndb.DateTimeProperty()

    def created_time_localed(self, member):
        return time_localed(self.created_time, member)

    def updated_time_localed(self, member):
        return time_localed(self.updated_time, member)

    def touched_time_localed(self, member):
        return time_localed(self.touched_time, member)

    #if member votes return false,else add and return true
    def vote_up_by(self, member):
        vote_up_members = memcache.get('Topic_'+str(self.key.id())+'_vote_up')
        if vote_up_members:
            if member.key.id() in vote_up_members:
                return False
            else:
                vote_up_members.append(member.key.id())
        else:
            vote_up_members = [member.key.id()]
        memcache.set('Topic_'+str(self.key.id())+'_vote_up', vote_up_members, time=60*60*24*20)
        self.votes += 1
        self.put()
        return True

    def vote_down_by(self, member):
        vote_down_members = memcache.get('Topic_'+str(self.key.id())+'_vote_down')
        if vote_down_members:
            if member.key.id() in vote_down_members:
                return False
            else:
                vote_down_members.append(member.key.id())
        else:
            vote_down_members = [member.key.id()]
        memcache.set('Topic_'+str(self.key.id())+'_vote_down', vote_up_members, time=60*60*24*20)
        self.votes -= 1
        self.put()
        return True

    def hits_by_ip(self, ip):
        hits_ips = memcache.get('Topic_'+str(self.key.id())+'_hits')
        print hits_ips
        if hits_ips:
            if ip in hits_ips:
                return False
            else:
                hits_ips.append(ip)
        else:
            hits_ips = [ip]
        print hits_ips
        memcache.set('Topic_'+str(self.key.id())+'_hits', hits_ips, time=60*60*24*20)
        self.hits += 1
        self.put()
        return True

class Amend(ndb.Model):
    topic_key = ndb.KeyProperty(kind=Topic)
    member_key = ndb.KeyProperty(kind=Member)
    #tag用于标记语法问题点
    tags = ndb.StringProperty(repeated=True)
    has_content = ndb.BooleanProperty(required=True, default=True)
    content = ndb.TextProperty()
    content_rendered = ndb.TextProperty()
    content_length = ndb.IntegerProperty(required=True, default=0)
    stars = ndb.IntegerProperty(required=True, default=0)
    replies = ndb.IntegerProperty(default=0)
    created_by = ndb.StringProperty(indexed=True)
    last_reply_by = ndb.StringProperty(indexed=True)
    source = ndb.StringProperty(indexed=True) #TODO
    explicit = ndb.IntegerProperty(required=True, default=0)
    created_time = ndb.DateTimeProperty(auto_now_add=True)
    updated_time = ndb.DateTimeProperty(auto_now=True)
    touched_time = ndb.DateTimeProperty()
    highlighted = ndb.BooleanProperty(required=True, default=False)

class Reply(ndb.Model):
    topic_key = ndb.KeyProperty(kind=Topic)
    amend_key = ndb.KeyProperty(kind=Amend)
    member_key = ndb.KeyProperty(kind=Member)
    content = ndb.TextProperty()
    source = ndb.StringProperty(indexed=True)
    created_by = ndb.StringProperty(indexed=True)
    created_time = ndb.DateTimeProperty(auto_now_add=True)
    updated_time = ndb.DateTimeProperty(auto_now=True)
    highlighted = ndb.BooleanProperty(required=True, default=False)

class Avatar(ndb.Model):
    num = ndb.IntegerProperty(indexed=True)
    name = ndb.StringProperty(indexed=True)
    content = ndb.BlobProperty()

"""
site:用于存放网站的信息，一个实例
"""
class Site(ndb.Model):
    title = ndb.StringProperty()
    slogan = ndb.StringProperty()
    description = ndb.TextProperty()
    domain = ndb.StringProperty()
    analytics = ndb.StringProperty()
    home_categories = ndb.TextProperty()
    meta = ndb.TextProperty(default='')
    home_top = ndb.TextProperty(default='')
    theme = ndb.StringProperty(default='default')
    l10n = ndb.StringProperty(default='zh_CN')
    location = ndb.StringProperty(default='Asia/Shanghai')
    use_topic_types = ndb.BooleanProperty(default=False)
    topic_types = ndb.TextProperty(default='')
    topic_view_level = ndb.IntegerProperty(required=True, default=-1)
    topic_create_level = ndb.IntegerProperty(required=True, default=1000)
    topic_reply_level = ndb.IntegerProperty(required=True, default=1000)
    data_migration_mode = ndb.IntegerProperty(required=True, default=0)
    created_time = ndb.DateTimeProperty(auto_now_add=True)
    updated_time = ndb.DateTimeProperty(auto_now=True)


