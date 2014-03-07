# -*- coding: utf-8 -*- 

import webapp2
import urllib
import json

from view.J2_env import J2_env

from google.appengine.datastore.datastore_query import Cursor
from model.db import Section,Node,Topic
from model.l10n import *
from model.util.security import *
from model.util.common import *

import BaseHandlers

class MainRouterHandler(BaseHandlers.BaseHandler):
    def get(self,section_name):
        member = CheckAuth(self)
        node_name = CheckNodeName('', member)
        self.redirect('/%s/%s'%(section_name, node_name))


class MainHandler(BaseHandlers.BaseHandler):
    def get(self, section_name, current_node_name):
        section_name = str(urllib.unquote(section_name))
        if current_node_name:
            current_node_name = str(urllib.unquote(current_node_name))
        cursor = Cursor(urlsafe=self.request.get('cursor'))

        member = CheckAuth(self)
        template_values = CreateBaseTemplateValues(self, member)
        template_values['member'] = member

        section = CheckSectionName(section_name)
        if not section:
            return self.redirect('/')
        nodes = Node.getsBySection(section)
        template_values['section'] = section
        template_values['nodes'] = nodes

        current_node_name = CheckNodeName(current_node_name, member)
        for node in nodes:
            if node.name == current_node_name:
                current_node = node
                template_values['current_node'] = current_node
        #get infos from db
        topics,next_cursor,has_more = Topic.query(Topic.node_key==current_node.key).order(Topic.created_time).fetch_page(20, start_cursor=cursor)
        template_values['topics'] = topics
        template_values['next_cursor'] = next_cursor
        template_values['has_more'] = has_more
        #show errors
        if 'errors' in self.session:
            template_values['errors'] = self.session['errors']
            template_values['error_messages'] = self.session['error_messages']
            del self.session['errors']
            del self.session['error_messages']
        if 'message'in self.session:
            template_values['messages'] = [self.session['message']]
            del self.session['message']
            
        if section_name == 'exchange':
            template = J2_env.get_template('lang_exchange.html')
        elif section_name == 'question':
            template = J2_env.get_template('lang_question.html')
        elif section_name == 'culture':
            template = J2_env.get_template('lang_culture.html')
        self.response.write(template.render(template_values))

class ContentReceiveHandler(BaseHandlers.BaseHandler):
    def post(self,section_name):
        section_name = str(urllib.unquote(section_name))
        member = member_required(self)
        if not member:
            return
        title = self.request.get('title','')
        content = self.request.get('content','')
        node_id = self.request.get('node_id','')
        site = GetSite()
        l10n = GetMessages(member=member,site=site)

        #check errors
        errors = 0
        error_messages = []
        if len(title) < 3:
            errors += 1
            error_messages.append(l10n.title_too_short)
        elif len(title) > 128:
            errors += 1
            error_messages.append(l10n.title_too_long)
        node = Node.get_by_id(int(node_id))
        if not node:
            errors += 1
            error_messages.append(l10n.system_error)
        #get section from db
        q_sections = Section.query(Section.name==section_name)
        if q_sections.count() > 0:
            section = q_sections.get()
        else:
            errors += 1
            error_messages.append(l10n.system_error)

        #add error info to session
        if errors:
            self.session['errors'] = errors
            self.session['error_messages'] = error_messages
        else:
            #add topic into db
            topic = Topic()
            topic.node_key = node.key
            topic.member_key = member.key
            topic.title = title
            topic.has_content = True if len(content) > 0 else False
            topic.content = content
            topic.content_length = len(content)
            topic.put()
            self.session['message'] = l10n.send_successful

        self.redirect('/%s/%s'%(section_name,node.name))

class VoteTopicHandler(BaseHandlers.BaseHandler):
    def post(self):
        member = member_required(self)
        if not member:
            return
        action = self.request.get('action','up').upper()
        topic_id = self.request.get('tpoic_id')
        action = 'UP' if action not in ['DOWN','UP']
        if topic_id:
            topic = Topic.get_by_id(topic_id)
            if action == 'UP':
                result = topic.vote_up_by(member)
            else:
                result = topic.vote_down_by(member)
        else:
            result = False
        data = {'result':result}
        self.response.write(json.dumps(data))