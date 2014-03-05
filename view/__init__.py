#encoding:utf-8

# from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.babel import Babel
# from flask_login import LoginManager
# from flask.ext.babel import gettext as _
# from view.util.files import AvatarManager

# app = Flask(__name__)

# app.config.from_object('view.flask_config.DevConfig')

# db = SQLAlchemy(app)

# babel = Babel(app)

# avatar = AvatarManager(app)

# login_manager = LoginManager()
# login_manager.setup_app(app)
# login_manager.login_view = "login"
# login_manager.login_message = _(u"Please log in to access this page.")
# login_manager.login_message_category = "info"
# #####################
# #####################

# import view.index
# import view.signup
# import view.login
# import view.twitter
# import view.mail
# import view.user