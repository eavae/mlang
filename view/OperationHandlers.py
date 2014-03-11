# -*- coding: utf-8 -*- 

import webapp2
import urllib
import json

from view.J2_env import J2_env

from google.appengine.datastore.datastore_query import Cursor
from model.db import Section,Node,Topic,Amend
from model.l10n import *
from model.util.security import *
from model.util.common import *

import BaseHandlers

class OperationHandler(BaseHandlers.BaseHandler):
    def get(self):
    	member = CheckAuth(self)
        action = self.request.get('action')
        id = int(self.request.get('id'))
        data = {}
        print action,id
        if action.lower() == 'topic_vote_up':
        	if not member:
        		self.abort(403)
        		return
        	else:
        		topic = Topic.get_by_id(id)
        		print topic
        		if topic:
        			result = topic.vote_up_by(member)
        		else:
        			result = False
        		data['result'] = result
        elif action.lower() == 'topic_vote_down':
        	if not member:
        		self.abort(403)
        		return
        	else:
        		topic = Topic.get_by_id(id)
        		if topic:
        			result = topic.vote_down_by(member)
        		else:
        			result = False
        		data['result'] = result
        elif action.lower() == 'amend_vote_up':
        	if not member:
        		self.abort(403)
        		return
        	else:
        		amend = Amend.get_by_id(id)
        		if amend:
        			result = amend.vote_up_by(member)
        		else:
        			result = False
        		data['result'] = result
        elif action.lower() == 'amend_vote_down':
        	if not member:
        		self.abort(403)
        		return
        	else:
        		amend = Amend.get_by_id(id)
        		if amend:
        			result = amend.vote_down_by(member)
        		else:
        			result = False
        		data['result'] = result

        self.response.write(json.dumps(data))
