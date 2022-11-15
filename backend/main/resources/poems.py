from flask import request, jsonify
from flask_restful import Resource
from .. import db
from sqlalchemy import Identity, func
from datetime import *
from main.models import PoemModel
from main.models import UserModel
from main.models import MarkModel
from sqlalchemy import func
from datetime import *
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required

class Poem(Resource):

    @jwt_required()
    def get(self, id):
        claims = get_jwt()
        if 'role' in claims:
            if claims['role'] == 'admin':
                poem = db.session.query(PoemModel).get_or_404(id)
                return poem.to_json()
        else:
            poem = db.session.query(PoemModel).get_or_404(id)
            return poem.to_json()            

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        id_user = get_jwt_identity()
        poem = db.session.query(PoemModel).get_or_404(id)
        if 'role' in claims:
            if claims['role'] == 'admin' or id_user == int(poem.userid):
                db.session.delete(poem)
                db.session.commit()
                return '', 204
            else:
                return 'User not authorized'

class Poems(Resource):

    @jwt_required(optional=True)
    def get(self):
        poems = db.session.query(PoemModel)
        page = 1
        per_page = 10
        claims = get_jwt()
        identity_user = get_jwt_identity()
        if identity_user:
            if request.get_json():
                filters = request.get_json().items()
                for key, value in filters:

                    if key == 'page':
                        page = int(value)
                    if key == 'per_page':
                        per_page = int(value)
            
            poems = db.session.query(PoemModel).filter(PoemModel.userid != identity_user)
            poems = poems.outerjoin(PoemModel.marks).groupby(PoemModel.id).order_by(func.count(PoemModel.marks))

        else:
            if request.get_json():
                filters = request.get_json().items()
                for key, value in filters:
                    
                    if key == 'page':
                        page = int(value)
                    if key == 'per_page':
                        per_page = int(value)

                    if key == 'title':
                        poems = poems.filter(PoemModel.title.like('%'+value+"%"))
                    if key == 'userid':
                        poems = poems.filter(PoemModel.userid == value)

                    if key == 'datetime[gt]':
                        poems = poems.filter(PoemModel.datetime >= datetime.strptime(value, '%d-%m-%Y'))
                    if key == 'datetime[lt]':
                        poems = poems.filter(PoemModel.datetime <= datetime.strptime(value, '%d-%m-%Y'))
                    if key == 'username':
                        poems = poems.username(PoemModel.user.has(UserModel.username.like('%'+value+'%')))

                    if key == 'sort_by':

                        if value == 'datetime':
                            poems = poems.order_by(PoemModel.datetime)
                        if value == 'datetime[desc]':
                            poems = poems.order_by(PoemModel.datetime.desc())
                        if value == 'mark':
                            poems = poems.outerjoin(PoemModel.marks).groupby(PoemModel.id).order_by(func.mean(MarkModel.score))
                        if value == 'mark[desc]':
                            poems = poems.outerjoin(PoemModel.marks).groupby(PoemModel.id).order_by(func.mean(MarkModel.score).desc())
                        if value == 'name':
                            poems = poems.order_by(PoemModel.user)
                        if value == 'name[desc]':
                            poems = poems.order_by(PoemModel.user.desc())

        poems = poems.paginate(page, per_page, True, 30)
        if 'role' in claims:
            if claims['role'] == 'admin':
                return jsonify({'poems': [poem.to_json_short() for poem in poems.items],
                'total': poems.total, 'pages': poems.pages, 'page': page})
            else:
                return jsonify({'poems': [poem.to_json_short() for poem in poems.items],
                'total': poems.total, 'pages': poems.pages, 'page': page})

    @jwt_required()
    def post(self):
        id_user = get_jwt_identity()
        poem = PoemModel.from_json(request.get_json())
        user = db.session.query(UserModel).get_or_404(id_user)
        claims = get_jwt()
        if 'role' in claims:
            if claims['role'] == 'poet':
                if len(user.poems) == 0 or len(user.marks) >= 2:
                    poem.user_id = id_user
                    db.session.add(poem)
                    db.session.commit()
                    return poem.to_json(), 201
                else:
                    return 'Not enough scores from this user'
            else:
                return 'User not authorized for this action'