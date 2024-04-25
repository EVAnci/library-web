from flask_restful import Resource
from flask import request, jsonify
from main.models import UserModel
from .. import db

# Test JSON Data

USERS = {
    1:{'name':'user1', 'rol':'user'},
    2:{'name':'user2', 'rol':'user'},
    3:{'name':'user3', 'rol':'user'},
    4:{'name':'admin', 'rol':'admin'},
}

class User(Resource):
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()
    
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return user.to_json(), 204
    
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json() , 201 

class Users(Resource):
    def get(self):
        users = db.session.query(UserModel).all()
        return jsonify([user.to_json() for user in users])
    
    def post(self):
        user = UserModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201