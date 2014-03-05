#coding:utf-8
from model import db
from view import app
from flask.ext.babel import format_timedelta,format_datetime
from datetime import datetime

class TAmend(db.Model):
    __tablename__ = "tamend"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    twitter_id = db.Column(db.Integer,db.ForeignKey('twitter.id'))
    content = db.Column(db.String(app.config['TEXT_MAX_LENGTH']))
    explain = db.Column(db.String(app.config['TEXT_MAX_LENGTH']))
    time = db.Column(db.DateTime)
    user = db.relationship('User',backref=db.backref('amends',lazy='dynamic'))
    twitter = db.relationship('Twitter',backref=db.backref('amends',lazy='dynamic'))

    def __init__(self,user,twitter,content,explain):
        self.user_id = user.id
        self.twitter_id = twitter.id
        self.content = content
        self.explain = explain
        self.time = datetime.utcnow()
        self.user = user
        self.twitter = twitter

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def getDict(self):
        data = {}
        data['id'] = self.id
        data['uid'] = self.user_id
        data['twitter_id'] = self.twitter_id
        data['content'] = self.content
        data['explain'] = self.explain
        data['datetime'] = format_datetime(self.time)
        data['timedelta'] = format_timedelta(datetime.utcnow() - self.time)
        return data

    @classmethod
    def getById(cls,id):
        return cls.query.filter_by(id=id).first()