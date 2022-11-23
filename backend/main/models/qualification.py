from .. import db

class Qualification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    poem_id = db.Column(db.Integer, db.ForeignKey('poem.id'), nullable=False)

    user = db.relationship('User', back_populates="qualifications", uselist=False, single_parent=True)
    poem = db.relationship('Poem', back_populates="qualifications", uselist=False, single_parent=True)

    def __repr__(self):
        return f'<Score: {self.score}, Comment: {self.comment}, User id: {self.user_id}, Poem id {self.poem_id}>'

    def to_json_complete(self):
        poem = poem.to_json()
        user = [users.to_json() for users in self.user]
        qualification_json = {
            'id': self.id,
            'name': str(self.name),
            'role': str(self.role),
            'email': str(self.email),
            'poem' : poem,
            'user' : user
        }
        return qualification_json

    def to_json(self):
        qualification_json = {
            'id' : self.id,
            'score' : str(self.score),
            'comment' : str(self.comment),
            'user_id' : self.user_id,
            'poem_id' : self.poem_id
        }
        return qualification_json

    @staticmethod
    def from_json(qualification_json):
        id = qualification_json.get('id')
        score = qualification_json.get('score')
        comment = qualification_json.get('comment')
        poem_id = qualification_json.get('poem_id')
        user_id = qualification_json.get('user_id')
        user_name = qualification_json.get('user_name')
        return Qualification(id=id, score=score, comment=comment, poem_id=poem_id, user_id=user_id, user_name=user_name)