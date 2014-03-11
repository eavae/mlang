#!/usr/bin/python
# -*- coding: utf-8 -*- 

import webapp2
import urllib
import json

from view.J2_env import J2_env

from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from google.appengine.datastore.datastore_query import Cursor
from model.db import Section,Node,Topic,Amend,Feedback
from model.l10n import *
from model.util.security import *
from model.util.common import *

import BaseHandlers

class FeedbackHandler(BaseHandlers.BaseHandler,blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        member = CheckAuth(self)
        template_values = CreateBaseTemplateValues(self, member)
        template_values['member'] = member

        #there should render 20 pages feedbacks
        template_values['feedbacks'] = Feedback.query().order(Feedback.created_time).fetch(20)

        #show errors
        if 'errors' in self.session:
            template_values['errors'] = self.session['errors']
            template_values['error_messages'] = self.session['error_messages']
            del self.session['errors']
            del self.session['error_messages']
        if 'message'in self.session:
            template_values['messages'] = [self.session['message']]
            del self.session['message']
        
        template = J2_env.get_template('feedback.html')
        self.response.write(template.render(template_values))

    def post(self):
        member = CheckAuth(self)
        template_values = CreateBaseTemplateValues(self, member)
        l10n = template_values['l10n']
        title = self.request.get('title')
        content = self.request.get('content')
        email = self.request.get('email')
        phone = self.request.get('phone')

        try:
            upload_files = self.get_uploads('screen_short')
            blob_info = upload_files[0]
            if blob_info.content_type not in ['image/bmp','image/gif','image/jpeg','image/png']:
                blob_info.delete()
        except:
            blob_info = False

        if member.email:
            email = member.email

        errors = 0
        error_messages = []

        #check title error
        if len(title) < 3:
            errors += 1
            error_messages.append(l10n.title_too_short)
        else:
            if len(title) > 128:
                errors += 1
                error_messages.append(l10n.title_too_long)

        if not errors:
            #save into db
            feedback = Feedback()
            feedback.title = title
            feedback.content = content
            feedback.email = email
            feedback.phone = phone
            if blob_info:
                feedback.screen_short = str(blob_info.key())
            feedback.put()
            self.session['message'] = l10n.feedback_successful
        else:
            self.session['errors'] = errors
            self.session['error_messages'] = error_messages

        self.redirect('/feedback')