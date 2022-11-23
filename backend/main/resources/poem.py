from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemModel, UserModel, QualificationModel
import datetime
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

class Poem(Resource):
    def get(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        return poem.to_json_short()

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        user_id = get_jwt_identity()
        poem = db.session.query(PoemModel).get_or_404(id)
        if "role" in claims:
            if user_id == int(poem.user_id):
                db.session.delete(poem)
                db.session.commit()
                return '', 204
            else:
                return "Solo los poetas pueden eliminar"
                
    @jwt_required()
    def put(self, id):
        claims = get_jwt()
        user_id = get_jwt_identity()
        poem = db.session.query(PoemModel).get_or_404(id)
        data = request.get_json().items()
        if "role" in claims:
            if user_id == int(poem.user_id):
                for key, value in data:
                    setattr(poem,key,value)
        db.session.add(poem)
        db.session.commit()
        return poem.to_json(), 201 

class Poems(Resource):
    @jwt_required(optional=True)
    def get(self):
        poems = db.session.query(PoemModel)
        page = 1
        per_page = 5
        claims = get_jwt()
        identify_user = get_jwt_identity()
        if identify_user:
            if request.get_json():
                filters = request.get_json().items()
                for key, value in filters:
                    if key == "page":
                        page = int(value)
                    if key == "per_page":
                        per_page = int(value)
            poems = db.session.query(PoemModel).filter(PoemModel.user_id == identify_user)
            poems = poems.outerjoin(PoemModel.qualifications).group_by(PoemModel.id).order_by(func.count(PoemModel.qualifications))
        else:
            if request.get_json():
                filters = request.get_json().items()
                for key, value in filters:
                    if key == "page":
                        page = int(value)
                    if key == "per_page":
                        per_page = int(value)
                    if key == "title":
                        poems = poems.filter(PoemModel.title.like('%'+value+'%'))
                    if key == "user_id":
                        poems = poems.filter(PoemModel.user_id == value)
                    if key == "user_name":
                        poems = poems.user_name(PoemModel.user.has(UserModel.name.like('%'+value+'%')))
                    if key == "created[gt]":
                        poems = poems.filter(PoemModel.date_time >= datetime.strptime(value, '%d-%m-%Y'))
                    if key == "created[lt]":
                        poems = poems.filter(PoemModel.date_time <= datetime.strptime(value, '%d-%m-%Y'))
                    if key == "qualification":
                        poems = poems.outerjoin(PoemModel.marks).group_by(PoemModel.id).having(func.mean(QualificationModel.score).like(float(value)))
                    if key == "sort_by":
                        if value == "author":
                            poems = poems.order_by(PoemModel.user)
                        if value == "author[desc]":
                            poems = poems.order_by(PoemModel.user.desc())
                        if value == "date":
                            poems == poems.order_by(PoemModel.date_time)
                        if value == "date[desc]":
                            poems = poems.order_by(PoemModel.date_time.desc())
                        if value == "qualification":
                            poems = poems.outerjoin(PoemModel.qualifications).group_by(PoemModel.id).order_by(func.mean(QualificationModel.score))
                        if value == "qualification[desc]":
                            poems = poems.outerjoin(PoemModel.qualifications).group_by(PoemModel.id).order_by(func.mean(QualificationModel.score).desc())
        poems = poems.paginate(page, per_page, True, 30)
        if "role" in claims:
            if claims["role"] == "admin":
                return jsonify({
                    "poems":[poem.to_json() for poem in poems.items],
                    "total": poems.total, 
                    "pages": poems.pages, 
                    "page": page
                    })
            return jsonify({
                "poems":[poem.to_json_short() for poem in poems.items],
                "total": poems.total, 
                "pages": poems.pages, 
                "page": page
                })
        else:
            return jsonify({
                "poems":[poem.to_json_short() for poem in poems.items],
                "total": poems.total, 
                "pages": poems.pages, 
                "page": page
                })
            
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        poem = PoemModel.from_json(request.get_json())
        user = db.session.query(UserModel).get_or_404(user_id)
        claims = get_jwt()
        if "role" in claims:
            if claims["role"] == "poet":
                poem.user_id = user_id
                db.session.add(poem)
                db.session.commit()
                return poem.to_json(), 201
            else:
                return "Solo los poetas pueden crear"