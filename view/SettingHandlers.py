# -*- coding: utf-8 -*-

from view.J2_env import J2_env

import re
import uuid
import hashlib
import webapp2
import urllib

from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from model.util.security import member_required,SetAuth
from model.util.common import CreateBaseTemplateValues
from model.db import Member
from model.l10n import *

import BaseHandlers

class SettingsHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/settings/common')

class SettingCommonHandler(webapp2.RequestHandler):
    def get(self):
        member = member_required(self)
        if not member:
            return
        template_values = CreateBaseTemplateValues(self, member)
        template_values['member'] = member
        site = template_values['site']

        location = member.location if member.location else site.location

        template_values['native_lang_select'] = GetUserLangSelect('native_lang', member.native_lang)
        template_values['favorite_lang_select'] = GetUserLangSelect('favorite_lang', member.favorite_lang)
        template_values['location_select'] = GetLocationSelect(location)
        template_values['l10n_select'] = GetSystemLangSelect(member.l10n if member.l10n else site.l10n)
        template = J2_env.get_template('setting_common.html')
        self.response.write(template.render(template_values))

    def post(self):
        member = member_required(self)
        if not member:
            return
        template_values = CreateBaseTemplateValues(self, member)
        template_values['member'] = member
        template_values['messages'] = []

        site = template_values['site']
        l10n = template_values['l10n']
        supported_user_lang = GetSupportedUserLang()
        location = member.location if member.location else site.location

        form_native_lang = self.request.get('native_lang').strip()
        form_favorite_lang = self.request.get('favorite_lang').strip()
        form_location = self.request.get('location').strip()
        form_email = self.request.get('email').strip()
        form_website = self.request.get('website').strip()
        form_motto = self.request.get('motto')
        form_introduce = self.request.get('introduce')

        errors = 0
        error_messages = []

        #check lang,location,l10n error
        print form_native_lang, form_favorite_lang, form_location
        if form_native_lang not in supported_user_lang or \
            form_favorite_lang not in supported_user_lang or \
            form_location not in GetSupportedLocation():
            errors += 1
            error_messages.append(l10n.form_error_message)
        #check email error
        if errors == 0:
            if len(form_email) == 0:
                errors += 1
                error_messages.append(l10n.email_empty_error)
            else:
                if len(form_email) > 32:
                    errors += 1
                    error_messages.append(l10n.email_too_long)
                else:
                    p = re.compile(r"(?:^|\s)[-a-z0-9_.+]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)", re.IGNORECASE)
                    if not p.search(form_email):
                        errors += 1
                        error_messages.append(l10n.email_not_validate)
        #check website error
        if errors == 0 and len(form_website) > 64:
            errors += 1
            error_messages.append(l10n.website_too_long)
        #check motto error
        if errors == 0 and len(form_motto) > 128:
            errors += 1
            error_messages.append(l10n.motto_too_long)
        #check introduce error
        if errors == 0 and len(form_introduce) > 256:
            errors += 1
            error_messages.append(l10n.introduce_too_long)

        if errors == 0:
            real_value = lambda a,b: a if a else b
            if member.email != form_email:
                member.email_verified = False
            member.native_lang = real_value(form_native_lang, member.native_lang)
            member.favorite_lang = real_value(form_favorite_lang, member.favorite_lang)
            member.location = real_value(form_location, member.location)
            member.email = real_value(form_email, member.email)
            member.website = real_value(form_website, member.website)
            member.motto = real_value(form_motto, member.motto)
            member.introduce = real_value(form_introduce, member.introduce)
            template_values['messages'].append(l10n.info_update_success)

        template_values['errors'] = errors
        template_values['error_messages'] = error_messages
        template_values['native_lang_select'] = GetUserLangSelect('native_lang', member.native_lang)
        template_values['favorite_lang_select'] = GetUserLangSelect('favorite_lang', member.favorite_lang)
        template_values['location_select'] = GetLocationSelect(location)
        template_values['l10n_select'] = GetSystemLangSelect(member.l10n if member.location else site.l10n)
        template = J2_env.get_template('setting_common.html')
        self.response.write(template.render(template_values))


class SettingPasswordHandler(webapp2.RequestHandler):
    def get(self):
        member = member_required(self)
        if not member:
            return
        template_values = CreateBaseTemplateValues(self, member)
        template_values['member'] = member

        template = J2_env.get_template('setting_password.html')
        self.response.write(template.render(template_values))

    def post(self):
        member = member_required(self)
        if not member:
            return
        template_values = CreateBaseTemplateValues(self, member)
        template_values['member'] = member
        template_values['messages'] = []

        errors = 0
        error_messages = []
        l10n = template_values['l10n']

        form_current_password = self.request.get('current_password')
        form_new_password = self.request.get('new_password')
        form_new_password_repeat = self.request.get('new_password_repeat')
        #check current password
        if len(form_current_password) == 0:
            errors += 1
            error_messages.append(l10n.password_empty_error)
        elif hashlib.sha1(form_current_password).hexdigest() != member.password:
            errors += 1
            error_messages.append(l10n.string_password_error)
        #check new password
        if errors == 0:
            if len(form_new_password) == 0:
                errors += 1
                error_messages.append(l10n.password_empty_error)
            else:
                if len(form_new_password) < 6:
                    errors += 1
                    error_messages.append(l10n.password_too_short)
                else:
                    if len(form_new_password) > 16:
                        errors += 1
                        error_messages.append(l10n.password_too_long)
                    else:
                        if form_new_password != form_new_password_repeat:
                            errors += 1
                            error_messages.append(l10n.password_not_same)
        #insert into db, update auth, reauth
        if errors == 0:
            member.password = hashlib.sha1(form_new_password).hexdigest()
            member.auth = hashlib.sha1(str(uuid.uuid1())+':'+form_new_password).hexdigest()
            member.put()
            SetAuth(self, member)
            template_values['messages'].append(l10n.password_update_success)
        template_values['errors'] = errors
        template_values['error_messages'] = error_messages
        template = J2_env.get_template('setting_password.html')
        self.response.write(template.render(template_values))

class SettingAvatarHandler(BaseHandlers.BaseHandler):
    def get(self):
        member = member_required(self)
        if not member:
            return
        template_values = CreateBaseTemplateValues(self, member)
        template_values['member'] = member
        template_values['upload_url'] = blobstore.create_upload_url('/settings/avatar_upload')
        template_values['messages'] = []

        if 'message' in self.session:
            template_values['messages'].append(self.session['message'])
            del self.session['message']

        template = J2_env.get_template('setting_avatar.html')
        self.response.write(template.render(template_values))


class AvatarUploadHandler(blobstore_handlers.BlobstoreUploadHandler,BaseHandlers.BaseHandler):
    def post(self):
        member = member_required(self)
        if not member:
            return
        template_values = CreateBaseTemplateValues(self, member)
        l10n = template_values['l10n']
        errors = 0
        #1.check accept error
        try:
            upload_files = self.get_uploads('avatar')  # 'avatar' is file upload field in the form
        except:
            errors += 1
            message = l10n.avatar_accept_error
        if errors == 0 and not upload_files:
            errors += 1
            message = l10n.avatar_accept_error

        if errors == 0:
            try:
                blob_info = upload_files[0]
            except:
                errors += 1
                message = l10n.avatar_accept_error
            #2.TODO:check mini type
            if blob_info.content_type not in ['image/bmp','image/gif','image/jpeg','image/png']:
                errors += 1
                message = l10n.avatar_type_error

        if errors == 0:
            #delete old avatar in blob
            if member.avatar:
                old_avatar_info = blobstore.BlobInfo.get(blobstore.BlobKey(member.avatar))
                if old_avatar_info:
                    old_avatar_info.delete()
            #insert avatar key into db
            member.avatar = str(blob_info.key())
            member.put()
            message = l10n.avatar_set_success
        self.session['message'] = message
        self.redirect('/settings/avatar')

class AvatarServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, size, resource):
        resource = str(urllib.unquote(resource))
        size = str(urllib.unquote(size))
        blob_info = blobstore.BlobInfo.get(resource)
        #73 48 24
        if size == 'large':
            size = 73
        elif size == 'normal':
            size = 48
        else:
            size = 24
        if blob_info:
            img = images.Image(blob_key=resource)
            img.resize(width=size, height=size)
            thumbnail = img.execute_transforms(output_encoding=images.PNG)
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(thumbnail)
            return
        self.send_blob(blob_info)
