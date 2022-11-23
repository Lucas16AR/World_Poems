from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import QualificationModel, PoemModel, UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

class Qualification(Resource):

    def get(self, id):
        qualification = db.session.query(QualificationModel).get_or_404(id)
        return qualification.to_json()

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        user_id = get_jwt_identity()
        qualification = db.session.query(QualificationModel).get_or_404(id)
        if "role" in claims:    
            if user_id == qualification.user_id:
                db.session.delete(qualification)
                db.session.commit()
                return '', 204
            else:
                return "Borrado de calificaciones solo para poemas"
    
    @jwt_required()
    def put(self, id):
        user_id = get_jwt_identity()
        qualification = db.session.query(QualificationModel).get_or_404(id)
        if user_id == qualification.user_id:
            data = request.get_json().items()
            for key, value in data:
                setattr(qualification, key, value)
            db.session.add(qualification)
            db.session.commit() 
            return qualification.to_json(), 201   
        else:
            return "Modificacion de calificaciones solo para poetas"

class Qualifications(Resource):
    def get(self):
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == "poem_id":
                    return self.show_marks_by_poem_id(value)
                if key == "user_id":
                    return self.show_marks_by_user_id(value)

        qualifications = db.session.query(QualificationModel).all()
        return jsonify([qualification.to_json() for qualification in qualifications])

    def show_marks_by_poem_id(self, id):
        qualifications = db.session.query(QualificationModel)
        qualifications = qualifications.filter(QualificationModel.poem.has(PoemModel.id == id)).all()
        return jsonify([qualification.to_json() for qualification in qualifications])

    def show_marks_by_user_id(self, id):
        qualifications = db.session.query(QualificationModel)
        qualifications = qualifications.filter(QualificationModel.user.has(UserModel.id == id)).all()
        return jsonify([qualification.to_json() for qualification in qualifications])

    @jwt_required()
    def post(self):
        qualification = QualificationModel.from_json(request.get_json())
        claims = get_jwt()
        if "role" in claims:
            if claims["role"] == "poet":
                db.session.add(qualification)
                db.session.commit()
                return qualification.to_json(), 201
            else:
                return "Comentarios solo para usuarios"
        else:
            return "Registrese"