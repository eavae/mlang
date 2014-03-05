#coding:utf-8
from model import db
from view import app
from sqlalchemy import desc
from flask.ext.babel import format_timedelta,format_datetime
from datetime import datetime

class Twitter(db.Model):
    __tablename__ = "twitter"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    content = db.Column(db.String(app.config['TEXT_MAX_LENGTH']))
    language = db.Column(db.String(10))
    time = db.Column(db.DateTime)
    user = db.relationship('User',backref=db.backref('twitters',lazy='dynamic'))

    def __init__(self,user,content,language):
        self.user_id = user.id
        self.content = content
        self.language = language
        self.time = datetime.utcnow()
        user = user

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def getDict(self):
        data = {}
        data['uid'] = self.user_id
        data['id'] = self.id
        data['content'] = self.content
        data['language'] = self.language
        data['datetime'] = format_datetime(self.time)
        data['timedelta'] = format_timedelta(datetime.utcnow() - self.time)
        return data

    @classmethod
    def getById(cls,id):
        return cls.query.filter_by(id=id).first()
        
    @classmethod
    def getAll(cls,lang='en',limit=30):
        return cls.query.filter_by(language=lang).order_by(desc(cls.time)).limit(limit).all()

    @classmethod
    def getByUser(cls,user,limit=30):
        return user.twitters.order_by(desc(cls.time)).limit(limit).all()