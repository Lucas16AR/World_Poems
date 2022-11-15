from xmlrpc.client import TRANSPORT_ERROR
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import MarkModel, UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import admin_required
from flask_mail import Mail
from main.mail.functions import sendMail

class Mark(Resource):

    @jwt_required(optional=True)
    def get(self, id):
        claims = get_jwt()
        if 'role' in claims:
            if claims['role'] == 'admin':
                mark = db.session.query(MarkModel).get_or_404(id)
                return mark.to_json()
        else:
            mark = db.session.query(MarkModel).get_or_404(id)
            return mark.to_json()

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        id_user = get_jwt_identity()
        mark = db.session.query(MarkModel).get_or_404(id)
        if 'role' in claims:
            if claims['role'] == 'admin' or id_user == mark.userid:
                db.session.delete(mark)
                db.session.commit()
                return '', 204
            else:
                return 'User not authorized to delete'

    @jwt_required()
    def put(self, id):
        id_user = get_jwt_identity()
        mark = db.session.query(MarkModel).get_or_404(id)
        if id_user == mark.userid:
            data = request.get_json().items()
            for key, value in data:
                setattr(mark, key, value)
            db.session.add(mark)
            db.session.commit()
            return 'User not authorized to create'

class Marks(Resource):
    @jwt_required(optional=True)
    def get(self):
        claims = get_jwt()
        if 'role' in claims:
            if claims['role'] == 'admin':
                marks = db.session.query(MarkModel)
                return jsonify([mark.to_json() for mark in marks])
            else:
                marks = db.session.query(MarkModel)
                return jsonify([mark.to_json() for mark in marks])
    
    @jwt_required()
    def post(self):
        id_user = get_jwt_identity()
        mark = MarkModel.from_json(request.get_json())
        user_mark = db.session.query(UserModel).get(id_user)
        claims = get_jwt()
        if 'role' in claims:
            if claims['role'] == 'poem':
                mark.userid = int(id_user)
                db.session.add(mark)
                db.session.commit()
                sent = sendMail([mark.poem.user.email], 'You received a mark', 'register', 
                user_mark = user_mark, 
                user = mark.poem.user, poem = mark.poem)
                return mark.to_json(), 201
            else:
                return 'User not authorized to post'