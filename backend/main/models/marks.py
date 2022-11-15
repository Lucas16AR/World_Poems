from .. import db
from sqlalchemy import column

class Mark(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    poemid = db.Column(db.Integer, db.ForeignKey("poem.id"), nullable = False)
    score = db.Column(db.Integer, nullable = False)
    comment = db.Column(db.String(255), nullable = False)

    user = db.relationship('User', back_populates = 'marks', uselist = False, single_parent = True)
    poem = db.relationship('Poem', back_populates = 'marks', uselist = False, single_parent = True)

    def __repr__(self):
        score_json = {
            'id': self.id,
            'score': self.score,
            'comment': self.comment,
            'user': [user.to_json_short() for user in self.user],
            'poem': [poem.to_json_short() for poem in self.poem]
        }
        return score_json

    def to_json(self):
        mark_json = {
            'id': self.id,
            'score': str(self.score),
            'comment': str(self.comment),
            'userid': self.user.to_json(),
            'poemid': self.poem.to_json()
        }
        return mark_json

    def to_json_complete(self):
        poem = poem.to_json()
        user = [user.to_json() for user in self.users]
        score_json = {
            'id': self.id,
            'name': str(self.name),
            'password': str(self.password),
            'role': str(self.role),
            'email': str(self.email),
            'poem': poem,
            'user': user
        }
        return score_json


    @staticmethod

    def from_json(mark_json):
        id = mark_json.get('id')
        score = mark_json.get('score')
        comment = mark_json.get('comment')
        userid = mark_json.get('userid')
        poemid = mark_json.get('poemid')
        return Mark(id=id,
            score=score,
            comment=comment,
            userid=userid,
            poemid=poemid
            )