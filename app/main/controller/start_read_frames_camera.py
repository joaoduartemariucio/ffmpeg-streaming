from flask import request
from flask_restful import Resource, reqparse
import threading
import base64

from app.main.service.video_frames_read_service import VideoFramesReadService

video_post_args = reqparse.RequestParser()
video_post_args.add_argument("video_url", type=str, help="link do video nao foi enviado", required=True)

thread_lock = threading.Lock()

global threads_abertas
threads_abertas = {}


class StartReadFramesCamera(Resource):

    def post(self):
        args = video_post_args.parse_args()
        video_url = str(args["video_url"])

        encoded = base64.b64encode(video_url.encode("utf-8"))
        frame_key = str(encoded, "utf-8")

        if frame_key in threads_abertas:
            return {"status": "THREAD_JA_INICIADA" , "key": frame_key} 
        else:
            init_thread(frame_key, video_url)
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

def init_thread(frame_key, video_url):
    thread = VideoFramesReadService(len(threads_abertas.keys()) + 1, frame_key, video_url, thread_lock)
    thread.start()
    threads_abertas[frame_key] = thread