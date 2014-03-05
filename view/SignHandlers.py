# -*- coding: utf-8 -*-
from view.J2_env import J2_env

import re
import hashlib
import uuid
import datetime
import webapp2

from google.appengine.api import memcache
from google.appengine.ext import ndb

from model.db import Counter,Member
from model.util.common import CreateBaseTemplateValues
from model.util.security import *


class SignupHandler(webapp2.RequestHandler):

    def get(self):
        member = CheckAuth(self)
        template_values = CreateBaseTemplateValues(self, member)
        template_values['member'] = member

        template = J2_env.get_template('signup.html')
        self.response.write(template.render(template_values))

    def post(self):
        member = CheckAuth(self)
        template_values = CreateBaseTemplateValues(self, member)
        template_values['member'] = member
        l10n = template_values['l10n']
        site = template_values['site']

        username = self.request.get('username').strip()
        email = self.request.get('email').strip()
        password = self.request.get('password')
        password_confirm = self.request.get('confirm')

        errors = 0
        error_messages = []
        #check username error
        if len(username) == 0:
            errors += 1
            error_messages.append(l10n.username_empty_error)
        else:
            if len(username) > 16:
                errors += 1
                error_messages.append(l10n.username_too_lang)
            else:
                if len(username) < 4:
                    errors += 1
                    error_messages.append(l10n.username_too_short)
                else:
                    if re.search('^[a-zA-Z0-9\_]+$', username):
                        q_members = Member.query(Member.username_lower == username.lower())
                        if q_members.count() > 0:
                            errors += 1
                            error_messages.append(l10n.username_repeated_error)
                    else:
                        errors += 1
                        error_messages.append(l10n.username_not_validate)
        #check password errors
        if errors == 0:
            if len(password) == 0:
                errors += 1
                error_messages.append(l10n.password_empty_error)
            else:
                if len(password) < 6:
                    errors += 1
                    error_messages.append(l10n.password_too_short)
                else:
                    if len(password) > 16:
                        errors += 1
                        error_messages.append(l10n.password_too_long)
                    else:
                        if password != password_confirm:
                            errors += 1
                            error_messages.append(l10n.password_not_same)
        #check email error
        if errors == 0:
            if len(email) == 0:
                errors += 1
                error_messages.append(l10n.email_empty_error)
            else:
                if len(email) > 32:
                    errors += 1
                    error_messages.append(l10n.email_too_long)
                else:
                    p = re.compile(r"(?:^|\s)[-a-z0-9_.+]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)", re.IGNORECASE)
                    if p.search(email):
                        q_members = Member.query(Member.email == email.lower())
                        if q_members.count() > 0:
                            errors += 1
                            error_messages.append(l10n.email_repeated_error)
                    else:
                        errors += 1
                        error_messages.append(l10n.email_not_validate)

        #if no errors, insert it into db
        if errors == 0:
            member = Member()
            q_counters = Counter.query(Counter.name == 'member_total')
            if q_counters == 1:
                counter = q_counters.get()
                counter.value += 1
            else:
                counter = Counter()
                counter.name = 'member_total'
                counter.value = 1
            member = Member()
            member.username = username
            member.email = email.lower()
            member.password = hashlib.sha1(password).hexdigest()
            member.auth = hashlib.sha1(str(uuid.uuid1())+':'+password).hexdigest()
            member.l10n = site.l10n
            member.put()
            counter.put()
            SetAuth(self, member)
            template_values['member'] = member
            memcache.delete('member_total')

        template_values['errors'] = errors
        template_values['error_messages'] = error_messages

        template = J2_env.get_template('signup.html')
        self.response.write(template.render(template_values))

class SigninHandler(webapp2.RequestHandler):
    def get(self):
        member = CheckAuth(self)
        template_values = CreateBaseTemplateValues(self, member)
        template_values['member'] = member
        template_values['redirect_url'] = self.request.get('redirect_url', '/')

        template = J2_env.get_template('signin.html')
        self.response.write(template.render(template_values))

    def post(self):
        member = CheckAuth(self)
        template_values = CreateBaseTemplateValues(self, member)
        template_values['member'] = member
        l10n = template_values['l10n']

        email_or_username = self.request.get('email_or_username').strip()
        password = self.request.get('password')
        redirect_url = self.request.get('redirect_url')

        errors = 0
        error_messages = []
        if len(email_or_username) > 0 and len(password) > 0:
            passwd_sha1 = hashlib.sha1(password).hexdigest()
            if '@' in email_or_username:
                q_members = Member.query(ndb.AND(Member.email==email_or_username.lower(), Member.password==passwd_sha1))
            else:
                q_members = Member.query(ndb.AND(Member.username_lower==email_or_username.lower(), Member.password==passwd_sha1))
            if q_members.count() == 1:
                member = q_members.get()
                member.last_signin_time = datetime.datetime.now()
                member.put()
                SetAuth(self,member)

                host = self.request.host + '/'
                if redirect_url.rfind(host) >= 0 and (redirect_url.rfind('/signin') == -1):
                    self.redirect(str(redirect_url))
                else:
                    self.redirect('/')
            else:
                errors += 1
                error_messages.append(l10n.username_password_error)
        else:
            errors += 1
            error_messages.append(l10n.username_password_empty)
        template_values['errors'] = errors
        template_values['error_messages'] = error_messages
        template_values['redirect_url'] = redirect_url
        template = J2_env.get_template('signin.html')
        self.response.write(template.render(template_values))

class SignoutHandler(webapp2.RequestHandler):
    def get(self):
        member = member_required(self)
        template_values = CreateBaseTemplateValues(self, member)

        UnsetAuth(self)
        template = J2_env.get_template('signout.html')
        self.response.write(template.render(template_values))
