from flask import request
from flask_restful import Resource
from models.user import User, db
from models.base import to_dict
from datetime import datetime


class RegisterAPI(Resource):
    """
    Register API
    """
    @staticmethod
    def post():
        """
        Register
        :return: success or error message
        """
        json = request.get_json()
        try:
            user = User(
                username=json["username"],
                phone=json["phone"],
                email=json["email"],
                create_time=datetime.now()
            )
        except KeyError:
            return {"error": "Lack necessary argument"}, 406
        if User.query.filter_by(username=user.username).first() is not None:
            return {"error": "User name has already been taken."}, 403
        user.hash_password(json["password"])
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username=user.username).first()
        token = user.generate_token()
        user = to_dict(user)
        return {
            "token": token,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "own_agent_id": user["own_agent_id"]
            }}, 201
