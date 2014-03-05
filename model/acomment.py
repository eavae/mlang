#coding:utf-8
from model import db
from view import app
from flask.ext.babel import format_timedelta,format_datetime
from datetime import datetime

class AComment(db.Model):
    __tablename__ = "acomment"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    amend_id = db.Column(db.Integer,db.ForeignKey('tamend.id'))
    comment = db.Column(db.String(app.config['TEXT_MAX_LENGTH']))
    time = db.Column(db.DateTime)
    amend = db.relationship('TAmend',backref=db.backref('comments',lazy='dynamic'))
    user = db.relationship('User')

    def __init__(self,user,amend,comment):
        self.user_id = user.id
        self.amend_id = amend.id
        self.comment = comment
        self.time = datetime.utcnow()
        self.amend = amend
        self.user = user

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def getDict(self):
        data = {}
        data['id'] = self.id
        data['uid'] = self.user_id
        data['aid'] = self.amend_id
        data['comment'] = self.comment
        data['timedelta'] = format_timedelta(datetime.utcnow() - self.time)
        data['datetime'] = format_datetime(self.time)
        return data