#coding:utf-8
from model import db
from view import app
from flask_login import make_secure_token
from const import I18n
import uuid

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    nickname = db.Column(db.String(128))
    native = db.Column(db.String(64))
    learning = db.Column(db.String(64))
    locale = db.Column(db.String(64))
    timezone = db.Column(db.String(64))
    is_auth = db.Column(db.Boolean)
    token = db.Column(db.String(64))

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.locale = app.config['BABEL_DEFAULT_LOCALE']
        self.timezone = app.config['BABEL_DEFAULT_TIMEZONE']
        self.is_auth = app.config['DEFAULT_USER_AUTH']
        self.token = make_secure_token(email+password+str(uuid.uuid4()))

    def getDict(self):
        return {
            'id':self.id,
            'email':self.email,
            'nickname':self.nickname,
            'native':I18n.langFullName(self.native),
            'learning':I18n.langFullName(self.learning),
            'locale':I18n.localeFullName(self.locale),
            'timezone':self.timezone
        }

    def commit(self):
    	db.session.add(self)
        db.session.commit()

    def is_authenticated(self):
        return self.is_auth

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def get_auth_token(self):
        return self.token

    @classmethod
    def getById(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def getByEmail(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def getByToken(cls,token):
        return cls.query.filter_by(token=token).first()

class UserDetail(db.Model):
    __tablename__ = 'user_detail'
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    realname = db.Column(db.String(128))
    birth = db.Column(db.Date)
    gender = db.Column(db.String(2))
    job = db.Column(db.String(128))
    purpose = db.Column(db.String(128))
    presentation = db.Column(db.String(app.config['TEXT_MAX_LENGTH']))
    user = db.relationship('User',backref=db.backref('detail',lazy='dynamic'))

    def __init__(self,user,**kwargs):
        self.user_id = user.id
        if kwargs:
            self.realname = kwargs.get['realname']
            self.birth = kwargs.get['birth']
            self.gender = kwargs.get['gender']
            self.job = kwargs.get['job']
            self.purpose = kwargs.get['purpose']
            self.presentation = kwargs.get['presentation']
        self.user = user

    def commit(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def getById(cls,id):
        return cls.query.filter_by(user_id=id).first()