from flask import send_file, request
from flask_restful import Resource, reqparse
import threading
import base64
import cv2
import os

from app.main.service.video_frames_read_service import VideoFramesReadService
from app.main.service.video_frames_read_service import last_frame_camera

video_post_args = reqparse.RequestParser()
video_post_args.add_argument("video_url", type=str, help="link do video nao foi enviado", required=True)

thread_lock = threading.Lock()
threads = list()

global threads_abertas
threads_abertas = {}


class StartReadFramesCamera(Resource):

    def post(self):
        args = video_post_args.parse_args()
        video_url = str(args["video_url"])

        encoded = base64.b64encode(video_url.encode("utf-8"))
        frame_key = str(encoded, "utf-8")

        if frame_key in threads_abertas:
            print("THREAD_JA_INICIADA video_url: %s key: %s" % (video_url, frame_key))
            return {"status": "THREAD_JA_INICIADA" , "key": frame_key} 
        else:
            last_frame_camera[frame_key] = "CONECTANDO"
            thread = VideoFramesReadService(threads.count(self) + 1, frame_key, video_url, thread_lock)
            thread.start()

            threads.append(threads)
            threads_abertas[frame_key] = thread
            print("INICIANDO_THREAD video_url: %s key: %s" % (video_url, frame_key))
            return {"status": "INICIANDO_THREAD", "key": frame_key}


    def delete(self):

        frame_key = str(request.args.get("key"))

        if frame_key in threads_abertas:

            thread = threads_abertas[frame_key] 
            thread.stop_read_frames()
            threads_abertas.pop(frame_key, None)

            return {"status": "THREAD_PARADA", "key": frame_key}
        else: 
            return {"status": "THREAD_NAO_EXISTE", "key": "invalid"}