from threading import Thread
import time
import uuid
import io
import numpy as np
import cv2

class VideoRecording(Thread):
  def __init__(self, cap, out):
    super(VideoRecording, self).__init__()
    self.cap = cap
    self.out = out
  def run(self):
    while(self.cap.isOpened()):
      ret, frame = self.cap.read()
      if ret==True:
          frame = cv2.flip(frame,0)
          self.out.write(frame)
          if cv2.waitKey(1) & 0xFF == ord('q'):
              break
      else:
          break

class CarCamera():
  def __init__(self):
    self.video_path = time.strftime("%d-%m-%Y_%H:%M:%S", time.localtime())
    self.video_path = "./video/" + self.video_path + ".avi"

    self.cap = cv2.VideoCapture(self.gstreamer_pipeline(
      capture_width=640, capture_height=368, display_width=640, display_height=368, framerate=30, flip_method = 2
    ), cv2.CAP_GSTREAMER)

    self.out = cv2.VideoWriter(self.video_path, cv2.VideoWriter_fourcc(*'XVID'), 30.0, (640,368))

  def start_recording(self):
    self.thread = VideoRecording(self.cap, self.out)
    self.thread.start()
    
  def stop_recording(self):
    self.cap.release()
    self.out.release()
    self.thread.join()
    
  def capture_as_rgb_array(self):
    ret = False
    while ret == False:
      ret, img = self.cap.read()
    return img

  def gstreamer_pipeline (self, capture_width=3280, capture_height=2464, display_width=820, display_height=616, framerate=21, flip_method=0) :   
    return ('nvarguscamerasrc ! ' 
    'video/x-raw(memory:NVMM), '
    'width=(int)%d, height=(int)%d, '
    'format=(string)NV12, framerate=(fraction)%d/1 ! '
    'nvvidconv flip-method=%d ! '
    'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
    'videoconvert ! '
    'video/x-raw, format=(string)BGR ! appsink'  % (capture_width,capture_height,framerate,flip_method,display_width,display_height))
    
if __name__ == '__main__':
  camera = CarCamera()
  camera.start_recording()
  time.sleep(4)
  print("Img as array test:")
  print(camera.capture_as_rgb_array())
  time.sleep(4)
  camera.stop_recording()