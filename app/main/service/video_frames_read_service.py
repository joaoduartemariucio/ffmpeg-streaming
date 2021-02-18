#!/usr/bin/python
import cv2
import time
import threading
import os

global last_frame_camera
last_frame_camera = {}


class VideoFramesReadService(threading.Thread):

    def __init__(self, thread_id, name, video_url, thread_lock):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.capture = cv2.VideoCapture(video_url)
        self.status = 1
        self.thread_lock = thread_lock
        self.read_ativo = True

    def run(self):

        last_frame_camera[self.name] = "CONECTADO"
        while self.read_ativo:

            if not self.capture.isOpened():
                self.status = 0 
                last_frame_camera[self.name] = "FALHA_CONEXAO_CAMERA"
                break
            
            ret, frame = self.capture.read()

            if not ret:
                last_frame_camera[self.name] = "DESCONECTADO"
                break
            else:
                last_frame_camera[self.name] = frame


    def stop_read_frames(self):
        self.read_ativo = False
        self.status = 0
        time.sleep(1)
        last_frame_camera[self.name] = "CONEXAO_PARADA"

    def __del__(self):
        self.capture.release()
