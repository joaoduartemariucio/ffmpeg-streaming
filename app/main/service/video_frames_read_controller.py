#!/usr/bin/python
import cv2
import time
import threading
import os

global last_frame_camera
last_frame_camera = {}

class VideoFramesReadController(threading.Thread):

    def __init__(self, thread_id, name, video_url, thread_lock):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.video_url = video_url
        self.capture = cv2.VideoCapture(0)
        self.status = 1
        self.thread_lock = thread_lock
        self.read_ativo = True

    def run(self):

        self.capture = cv2.VideoCapture(self.video_url)
        
        while self.read_ativo:

            if not self.capture.isOpened():
                self.status = 0 
                last_frame_camera[self.name] = "THREAD_CAPTURA_FRAMES_PARADA"
                break
            
            ret, frame = self.capture.read()

            if not ret:
                print("Falha capturar frame")
                continue
            else:
                last_frame_camera[self.name] = frame


    def stop_read_frames(self):
        self.read_ativo = False
        self.status = 0
        time.sleep(1)
        last_frame_camera[self.name] = "THREAD_CAPTURA_FRAMES_PARADA"

    def __del__(self):
        self.capture.release()
