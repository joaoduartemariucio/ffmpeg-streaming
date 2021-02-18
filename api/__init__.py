from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Api
from api.routes.read_last_frame_camera import ReadLastFrameCamera
from api.routes.status_service import StatusService
from api.routes.start_read_frames_camera import StartReadFramesCamera
from api.config.config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    api = Api(app)

    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    base_resource_api = "/api/v1"

    api.add_resource(StatusService, f"{base_resource_api}/status")
    api.add_resource(ReadLastFrameCamera, f"{base_resource_api}/last_frame_video")
    api.add_resource(StartReadFramesCamera, f"{base_resource_api}/video_frame_capture_init")

    CORS(app)

    return app