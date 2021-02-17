from flask_restful import Resource


class StatusService(Resource):

    def get(self):
        return {"status": "servidor rodando"}
