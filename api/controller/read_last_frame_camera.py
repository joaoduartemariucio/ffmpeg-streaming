from flask import request, Response
from flask_restful import Resource
import cv2

from  api.service.video_frames_read_service import last_frame_camera


class ReadLastFrameCamera(Resource):

    def get(self):

        frame_key = str(request.args.get("key"))

        if frame_key in last_frame_camera:

            frame = last_frame_camera[frame_key]

            try:
                ret, jpeg = cv2.imencode('.jpg', frame)
                if not ret:
                    return {"status": "ERRO_CONVERSAO", "key": frame_key}
                else:
                    return Response(response=jpeg.tobytes(), status=200, mimetype="image/jpeg")
            except:
                return {"status": frame, "key": frame_key}
        else:
            return {"status": "NENHUM_FRAME_DISPONIVEL", "key": frame_key}, 404