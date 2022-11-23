from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel, UserModel
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from main.auth.decorators import admin_required

class User(Resource):
    @jwt_required(optional=True)
    def get(self, id):
        user_id = get_jwt_identity()
        user = UserModel.from_json(request.get_json())
        user = db.session.query(UserModel).get_or_404(user_id)
        claims = get_jwt()
        if "role" in claims:
            if claims["role"] == "poet":
                user.user_id = user_id
                db.session.add(user)
                db.session.commit()
                return user.to_json(), 201
        else:
            return user.to_json_short(), 201
    
    @jwt_required()
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json() , 201
    
    @jwt_required()
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class Users(Resource):
    @jwt_required()
    def get(self):
        page = 1
        per_page = 10
        users = db.session.query(UserModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == "page":
                    page = int(value)
                if key == "per_page":
                    per_page = int(value)
                if key == "name":
                    users = users.filter(UserModel.name.like('%'+value+'%'))
                if key == "sort_by":
                    if key == 'name':
                        users = users.order_by(UserModel.name)
                    if value == "num_users[desc]":
                        users = users.outerjoin(UserModel.users).group_by(UserModel.id).order_by(func.count(UserModel.id).desc())
                    if value == "num_users":
                        users = users.outerjoin(UserModel.users).group_by(UserModel.id).order_by(func.count(UserModel.id))
                    if value == "num_qualifications":
                        users = users.outerjoin(UserModel.qualifications).group_by(UserModel.id).order_by(func.count(UserModel.id).desc())
        users = users.paginate(page, per_page, True, 30)
        return jsonify({
            'users' : [user.to_json() for user in users.items],
            'total' : users.total,
            'pages' : users.pages,
            'page' : page
        })

    def post(self):
        user = UserModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201