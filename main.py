# -*- coding: utf-8 -*- 

import _env
import webapp2

from view.HomeHandler import HomeHandler
from view.SignHandlers import SignupHandler,SigninHandler,SignoutHandler
from view.SettingHandlers import SettingsHandler
from view.SettingHandlers import SettingCommonHandler
from view.SettingHandlers import SettingPasswordHandler
from view.SettingHandlers import SettingAvatarHandler
from view.SettingHandlers import AvatarUploadHandler
from view.SettingHandlers import AvatarServeHandler
from view.MainHandlers import MainHandler
from view.MainHandlers import MainRouterHandler
from view.MainHandlers import ContentReceiveHandler

# def install_secret_key(app, filename='secret_key'):
#     filename = os.path.join(app.instance_path, filename)
#     try:
#         app.config['SECRET_KEY'] = open(filename, 'rb').read()
#     except IOError:
#         print 'Error: No secret key. Create it with:'
#         if not os.path.isdir(os.path.dirname(filename)):
#             print 'mkdir -p', os.path.dirname(filename)
#         print 'head -c 24 /dev/urandom >', filename
#         sys.exit(1)
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'GÁßÿJXPâÛÊ¬°;éJÂ•£',
}

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/signup', SignupHandler),
    ('/signin', SigninHandler),
    ('/signout', SignoutHandler),
    ('/settings', SettingsHandler),
    ('/settings/common', SettingCommonHandler),
    ('/settings/password', SettingPasswordHandler),
    ('/settings/avatar', SettingAvatarHandler),
    ('/settings/avatar_upload', AvatarUploadHandler),
    ('/avatar/(large|normal|mini)/([^/]+)?', AvatarServeHandler),
    ('/(exchange|question|culture)', MainRouterHandler),
    ('/post/(exchange|question|culture)', ContentReceiveHandler),
    ('/(exchange|question|culture)/([^/]+)?', MainHandler)
    ],
    debug=True,
    config=config)

def main():
    pass
if __name__ == "__main__":
    main()

# import sae
# import re
# from flask import request,redirect
# from flask_login import current_user
# from jinja2 import evalcontextfilter, Markup, escape
# from view import app,login_manager,babel
# from model import init_db
# from model.user import User

# init_db()

# @login_manager.user_loader
# def load_user(uid):
#     return User.getById(uid)

# @login_manager.unauthorized_handler
# def unauthorized():
#     return redirect('/email/send')

# @login_manager.token_loader
# def token_loader(token):
#     return User.getByToken(token)

# @babel.localeselector
# def get_locale():
#     #非隐身用户返回用户的区域
#     locale = request.accept_languages.best_match(['zh_CN','en','jo'])
#     if not current_user.is_anonymous:
#         locale = current_user.locale
#     return locale

# @babel.timezoneselector
# def get_timezone():
#     if not current_user.is_anonymous:
#         return current_user.timezone
#     return None

# # the nl2br filter
# _paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
# @app.template_filter()
# @evalcontextfilter
# def nl2br(eval_ctx, value):
#     result = u''.join(u'<p>%s</p>' % p.replace('\n', '<br>') for p in _paragraph_re.split(escape(value)))
#     if eval_ctx.autoescape:
#         result = Markup(result)
#     return result

# install_secret_key(app)
# application = sae.create_wsgi_app(app)


