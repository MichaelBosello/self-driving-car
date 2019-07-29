import time
import uuid
from picamera import PiCamera
import io
import numpy as np

class CarCamera():
  def __init__(self):
    self.video_path = time.strftime("%d-%m-%Y_%H:%M:%S", time.localtime())
    self.video_path = "./video/" + self.video_path + ".h264"

    self.camera = PiCamera()
    self.camera.resolution = (640, 360)
    self.camera.framerate = 30
    self.camera.start_preview()
    time.sleep(2)
    self.stream = picamera.array.PiRGBArray(self.camera)

  def start_recording(self):
    self.camera.start_recording(self.video_path)
    
  def stop_recording(self):
    self.camera.stop_recording()
    self.camera.stop_preview()
    
  def capture_as_rgb_array(self, resize = None):
    self.camera.capture(self.stream, format='rgb', resize=resize)
    return self.stream.array

  def capture_as_gray_array(self, resize = None):
    self.camera.capture(self.stream, format='rgb', resize=resize)
    return rgb2gray(self.stream.array)

  def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])
    
if __name__ == '__main__':
  camera = CarCamera()
  camera.start_recording()
  time.sleep(20)
  camera.stop_recording()