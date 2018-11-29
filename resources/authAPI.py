from flask import request, g
from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource
from models.user import User

acao = {"Access-Control-Allow-Origin": "*"}
auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    """
    Verify the token
    :param token: given token
    :return: bool
    """
    g.current_user = User.verify_token(token)
    return g.current_user is not None


class AuthAPI(Resource):
    """
    Authorization API
    """
    @staticmethod
    def post():
        """
        Login in
        :return: token or error message
        """
        username = request.json.get("username")
        password = request.json.get("password")
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {"error": "Username doesn't exist"}, 404, acao
        if not user.verify_password(password):
            return {"error": "Wrong password"}, 403, acao
        return {"token": user.generate_token()}, 201, acao
