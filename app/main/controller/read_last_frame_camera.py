from flask import send_file, request, Response
from flask_restful import Resource
import cv2
import os
import numpy as np
import datetime

from app.main.service.video_frames_read_controller import last_frame_camera


class ReadLastFrameCamera(Resource):

    def get(self):

        frame_key = str(request.args.get("key"))

        if frame_key in last_frame_camera:

            frame = last_frame_camera[frame_key]

            if frame == "THREAD_CAPTURA_FRAMES_PARADA":
                return {"status": "THREAD_CAPTURA_FRAMES_PARADA", "key": frame_key}, 406
            else:

                ret, jpeg = cv2.imencode('.jpg', frame)

                if not ret:
                    return {"status": "ERROR_GET_IMAGE", "key": frame_key}, 400
                else:
                    return Response(response=jpeg.tobytes(), status=200, mimetype="image/jpeg")
        else:
            return {"status": "NOT_EXIST_FRAME", "key": frame_key}, 404