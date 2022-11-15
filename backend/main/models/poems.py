from collections import UserList
from .. import db
from datetime import datetime
from sqlalchemy import column
import statistics
from statistics import mean

class Poem(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = True)
    title = db.Column(db.String(255), nullable = False)
    body = db.Column(db.String(255), nullable = False)
    datetime = db.Column(db.DateTime, nullable = False, default=datetime.now())

    user = db.relationship('User', back_populates = 'poems', uselist = False, single_parent = True)
    marks = db.relationship('Mark', back_populates = 'poem', cascade = 'all, delete-orphan')

    def __repr__(self):
        return '<Poem: %r %r >' % (self.userid, self.title, self.body, self.datetime)

    def score_mean(self):
        score_list = []
        if len(self.marks) == 0:
            mean = 0
        else:
            for mark in self.marks:
                score = mark.score
                score_list.append(score)
            mean = statistics.mean(score_list)
            return mean

    def to_json(self):
        poem_json = {
            'id': self.id,
            'title': str(self.title),
            'body': str(self.body),
            'user': self.user.to_json(),
            'datetime': str(self.datetime.strftime('%d-%m-%Y')),
            'marks': [mark.to_json() for mark in self.marks],
            'score_mean': self.score_mean()
        }
        return poem_json

    def to_json_short(self):
        poem_json = {
            'id': self.id,
            'title': str(self.title),
            'body': str(self.body)
        }
        return poem_json

    @staticmethod

    def from_json(poem_json):
        id = poem_json.get('id')
        userid = poem_json.get('userid')
        title = poem_json.get('title')
        body = poem_json.get('body')
        return Poem(id=id,
            userid=userid,
            title=title,
            body=body
            )