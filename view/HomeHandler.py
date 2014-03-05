# -*- coding: utf-8 -*- 

from view.J2_env import J2_env

import os
import webapp2

from google.appengine.api import memcache
from google.appengine.ext import ndb

from model.db import Counter
from model.util.common import CreateBaseTemplateValues
from model.util.security import SetAuth,CheckAuth

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        member = CheckAuth(self)
        template_values = CreateBaseTemplateValues(self, member)
        template_values['member'] = member

        if member:
            SetAuth(self, member)
            template_values['member'] = member

        member_total = memcache.get('member_total')
        if member_total is None:
            q_counters = Counter.query(Counter.name == 'member_total')
            if q_counters.count() > 0:
                member_total = q_counters.get().value
            else:
                member_total = 0
            memcache.set('member_total', member_total, 3600)
        template_values['member_total'] = member_total

        topic_total = memcache.get('topic_total')
        if topic_total is None:
            q_counters = Counter.query(Counter.name == 'topic_total')
            if q_counters.count() > 0:
                topic_total = q_counters.get().value
            else:
                topic_total = 0
            memcache.set('topic_total', topic_total, 3600)
        template_values['topic_total'] = member_total

        reply_total = memcache.get('reply_total')
        if reply_total is None:
            q_counters = Counter.query(Counter.name == 'reply_total')
            if q_counters.count() > 0:
                topic_total = q_counters.get().value
            else:
                topic_total = 0
            memcache.set('reply_total', reply_total, 3600)
        template_values['reply_total'] = reply_total

        amend_total = memcache.get('amend_total')
        if amend_total is None:
            q_counters = Counter.query(Counter.name == 'amend_total')
            if q_counters.count() > 0:
                amend_total = q_counters.get().value
            else:
                amend_total = 0
            memcache.set('amend_total', amend_total, 3600)
        template_values['amend_total'] = amend_total

        template = J2_env.get_template('index.html')
        self.response.write(template.render(template_values))

