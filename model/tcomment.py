#coding:utf-8
from model import db
from view import app
from flask.ext.babel import format_timedelta,format_datetime
from datetime import datetime

class TComment(db.Model):
    __tablename__ = "tcomment"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    twitter_id = db.Column(db.Integer,db.ForeignKey('twitter.id'))
    comment = db.Column(db.String(app.config['TEXT_MAX_LENGTH']))
    time = db.Column(db.DateTime)
    twitter = db.relationship('Twitter',backref=db.backref('comments',lazy='dynamic'))
    user = db.relationship('User')

    def __init__(self,user,twitter,comment):
        self.user_id = user.id
        self.twitter_id = twitter.id
        self.comment = comment
        self.time = datetime.utcnow()
        self.twitter = twitter
        self.user = user

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def getDict(self):
        data = {}
        data['cid'] = self.id
        data['uid'] = self.user_id
        data['tid'] = self.twitter_id
        data['comment'] = self.comment
        data['datetime'] = format_datetime(self.time)
        data['timedelta'] = format_timedelta(datetime.utcnow() - self.time)
        return data