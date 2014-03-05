#!/usr/bin/env python
#coding:utf-8
import os
import inspect
import jinja2

current = os.path.dirname(__file__)
app_root_dir = os.path.dirname(current)

J2_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(app_root_dir,'tpl')),
    extensions=['jinja2.ext.autoescape',
        'jinja2.ext.i18n'],
    autoescape=True)

J2_env.install_null_translations(newstyle=False)