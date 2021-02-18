from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Api
from multiprocessing import Process
from app.main.controller.read_last_frame_camera import ReadLastFrameCamera
from app.main.controller.status_service import StatusService
from app.main.controller.start_read_frames_camera import StartReadFramesCamera
import time
from app.main.config import config_by_name

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