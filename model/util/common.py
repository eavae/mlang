# -*- coding: utf-8 -*- 

import re

from google.appengine.api import memcache
from model.util.security import CheckAuth
from model.l10n import GetMessages

from model.db import Site,Section,Node

def IsMobileBowser(handler):
    user_agent = handler.request.headers['User-Agent']
    if (re.search('iPod|iPhone|Android|Opera Mini|BlackBerry|webOS|UCWEB|Blazer|PSP|IEMobile', user_agent)):
        return True
    else:
        return False

def GetSite():
    site = memcache.get('site')
    if site is not None:
        return site
    else:
        q_sites = Site.query().order(Site.created_time)
        if q_sites.count() == 1:
            site = q_sites.get()
            if site.l10n is None:
                site.l10n = 'zh_CN'
            memcache.set('site', site, 86400)
            return site
        else:
            site = Site()
            site.title = 'M-LANG'
            site.domain = 'mlang.appspot.com'
            site.slogan = 'a beautiful way to learn languages'
            site.l10n = 'zh_CN'
            site.location = 'Asia/Shanghai'
            site.description = ''
            site.meta = ''
            site.put()
            memcache.set('site', site, 86400)
            return site

def CreateBaseTemplateValues(handler, member = False):
    site = GetSite()
    l10n = GetMessages(member, site)

    template_values = {}
    template_values['is_mobile'] = IsMobileBowser(handler)
    template_values['ua'] = handler.request.headers['User-Agent']
    template_values['site'] = site
    template_values['page_title'] = site.title
    template_values['l10n'] = l10n
    return template_values

def CheckSectionName(section_name):
    if section_name not in ['exchange','question','culture']:
        return False
    q_sections = Section.query(Section.name==section_name)
    if q_sections.count() == 0:
        #insert default section
        section = Section(name=section_name)
        section.put()
        return section
    else:
        return q_sections.get()

def CheckNodeName(node_name, member=False):
    if node_name in ['en','zh_CN','ja']:
        return node_name
    elif member and member.favorite_lang:
        return member.favorite_lang
    else:
        return 'en'