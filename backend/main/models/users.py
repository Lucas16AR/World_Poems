from .. import db
from tokenize import generate_tokens
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)

    poems = db.relationship('Poem', back_populates = 'user', cascade = 'all, delete-orphan')
    marks = db.relationship('Mark', back_populates = 'user', cascade = 'all, delete-orphan')

    @property
    def plain_password(self):
        raise AttributeError('Password not readable')

    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)
    
    def validate_pass(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Name: {self.name}, email: {self.email}, password: {self.password}, role: {self.role}>'

    def to_json(self):
        user_json = {
            'id': self.id,
            'name': str(self.name),
            'num_poems': len(self.poems),
            'num_marks': len(self.marks),
            'poems': [poem.to_json_short() for poem in self.poems]
            }
        return user_json

    def to_json_short(self):
        user_json = {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
        return user_json

    def to_json_complete(self):
        poems = [poem.to_json() for poem in self.poems]
        marks = [mark.to_json() for mark in self.marks]
        user_json = {
            'id': self.id,
            'name': str(self.name),
            'password': str(self.password),
            'role': str(self.role),
            'email': str(self.email),
            'poems': poems,
            'marks': marks
        }
        return user_json

    @staticmethod
    
    def from_json(user_json):
        id = user_json.get('id')
        name = user_json.get('name')
        password = user_json.get('password')
        email = user_json.get('email')
        role = user_json.get('role')
        return User(id=id,
                name=name,
                plain_password=password,
                email=email,
                role=role
                )