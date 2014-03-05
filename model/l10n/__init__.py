# -*- coding: utf-8 -*- 
#
#"en":u"English (US)‎",
#        "zh_CN":u"中文（简体）‎",
#        "ja":u"日本語"
#
from pytz.gae import pytz

def GetMessages(member=False, site=False):
    if member:
        if member.l10n == 'zh_CN':
            from model.l10n.messages import zh_Hans as messages
            return messages
    else:
        if site.l10n == 'zh_CN':
            from model.l10n.messages import zh_Hans as messages
            return messages

def GetSupportedSystemLang():
    return {
        'zh_CN':u'简体中文'
    }

def GetSupportedUserLang():
    return {
        'en':u'English (US)‎',
        'zh_CN':u'中文（简体）‎',
        'ja':u'日本語'
    }

def GetUserLangSelect(name, current='zh_CN'):
    s = '<select name="' + name + '">'
    langs = GetSupportedUserLang()
    for key,value in langs.items():
        if key == current:
            s = s + '<option value="' + key + '" selected="selected">' + value + '</option>'
        else:
            s = s + '<option value="' + key + '">' + value + '</option>'
    s = s + '</select>'
    return s


def GetLocationSelect(current):
    s = '<select name="location">'
    for location in pytz.common_timezones:
        if location == current:
            s = s + '<option value="' + location + '" selected="selected">' + location + '</option>'
        else:
            s = s + '<option value="' + location + '">' + location +'</option>'
    s = s + '</select>'
    return s

def GetSupportedLocation():
    return pytz.common_timezones

def GetSystemLangSelect(current):
    lang = GetSupportedSystemLang()
    s = '<select name="l10n">'
    for l,n in lang.items():
        if lang == current:
            s = s + '<option value="' + l + '" selected="selected">' + n + '</option>'
        else:
            s = s + '<option value="' + l + '">' + n + '</option>'
    s = s + '</select>'
    return s