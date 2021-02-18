from flask_restful import Resource
from api.routes.start_read_frames_camera import threads_abertas

class StatusService(Resource):

    def get(self):
        
        return { 
            "status": "RODANDO", 
            "threads_abertas": f"{len(threads_abertas.keys())}" 
            }
