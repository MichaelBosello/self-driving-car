import time
import uuid
import picamera
import picamera.array
from picamera import PiCamera
import io
import numpy as np

class CarCamera():
  def __init__(self):
    self.video_path = time.strftime("%d-%m-%Y_%H:%M:%S", time.localtime())
    self.video_path = "./video/" + self.video_path + ".h264"

    self.camera = PiCamera()
    self.camera.resolution = (640, 368)
    self.camera.framerate = 30
    self.camera.start_preview()
    time.sleep(2)
    self.stream = picamera.array.PiRGBArray(self.camera)

    self.text_path = "./video/" + self.file_name + ".txt"
    self.text_file = open(self.text_path, "a")

  def start_recording(self):
    self.camera.start_recording(self.video_path)
    self.start_time = datetime.datetime.now()
    
  def stop_recording(self):
    self.camera.stop_recording()
    self.camera.stop_preview()
    self.text_file.close()
    
  def capture_as_rgb_array(self, resize = None):
    with picamera.array.PiRGBArray(self.camera) as stream:
      self.camera.capture(stream, format='rgb', resize=resize)
      return stream.array

  def capture_as_rgb_array_bottom_half(self):
      self.crop_bottom_half(self.capture_as_rgb_array())
  
  def crop_bottom_half(self, image):
      cropped_img = image[image.shape[0]/2:image.shape[0]]
      return cropped_img
    
if __name__ == '__main__':
  import cv2
  camera = CarCamera()
  camera.start_recording()
  time.sleep(4)
  print("Img as array test:")
  print(camera.capture_as_rgb_array())
  time.sleep(4)
  print("show cropped image")
  cv2.imshow('cropped', camera.capture_as_rgb_array_bottom_half())
  cv2.waitKey(20000)
  camera.stop_recording()