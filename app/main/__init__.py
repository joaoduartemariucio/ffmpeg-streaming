from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Api

from app.main.controller.read_last_frame_camera import ReadLastFrameCamera
from app.main.controller.status_service import StatusService
from app.main.controller.start_read_frames_camera import StartReadFramesCamera

from app.main.config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    api = Api(app)

    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    api.add_resource(StatusService, "/api/status")
    api.add_resource(ReadLastFrameCamera, "/api/last_frame_video")
    api.add_resource(StartReadFramesCamera, "/api/video_frame_capture_init")

    return app