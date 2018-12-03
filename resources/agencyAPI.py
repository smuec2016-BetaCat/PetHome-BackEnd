from flask import request
from flask_restful import Resource
from models.agency import Agency, db
from models.base import to_dict
from datetime import datetime

acao = {"Access-Control-Allow-Origin": "*"}


class AgencyAPI(Resource):
    @staticmethod
    def post():
        """
        Create a new agency
        :return: success or error message
        """
        json = request.get_json()
        try:
            agency = Agency(
                name=json["name"],
                introduction=json["introduction"],
                city=json["city"],
                address=json["address"],
                phone=json["phone"],
                create_time=datetime.now()
            )
        except KeyError:
            return {"error": "Lack necessary argument"}, 406, acao
        db.session.add(agency)
        db.session.commit()
        return {"msg": "Success"}, 201, acao
        

    @staticmethod
    def get():
        """
        Get agency information
        :return: agency information
        """
        args = request.args
        if "id" not in args:
            agency_list = Agency.query.all()
            for i in range(len(agency_list)):
                agency_list[i] = to_dict(agency_list[i])
            return {"agency_list": agency_list}, 200, acao
        agency = Agency.query.get(id=args["id"])
        if agency is None:
            return {"error": "Agency ID doesn't exist"}, 404, acao
        return {"agency": to_dict(agency)}, 200, acao
