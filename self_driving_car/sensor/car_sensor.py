def CarSensor(car_type):
    if car_type == 'hjduino':
      from sensor.car_sensor_hjduino import CarSensorHJduino
      return CarSensorHJduino(isJetson = True)
    if car_type == 'xiaor':
      from sensor.car_sensor_xiaor import CarSensorXiaoR
      return CarSensorXiaoR(isJetson = True)
    if car_type == 'picar':
      from sensor.car_sensor_picar import CarSensorPicar
      return CarSensorPicar(isRaspberry = True)


from abc import ABC, abstractmethod
import time
class CarSensorBase(ABC):
  def __init__(self, isJetson = False, isRaspberry = False):
    if isJetson:
      import Jetson.GPIO as GPIO
    if isRaspberry:
      import RPi.GPIO as GPIO

    self.GPIO = GPIO

    self.sensor_label = {
      self.distance_sensor_front() : "front_crash",
      self.lx_distance_sensor_front() : "front_lx_crash",
      self.rx_distance_sensor_front() : "front_rx_crash",
      self.lx_distance_sensor_back() : "back_lx_crash",
      self.rx_distance_sensor_back() : "back_rx_crash",
      self.lx_line_sensor() : "on_the_line_lx",
      self.rx_line_sensor() : "on_the_line_rx"
    }

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.distance_sensor_front(), GPIO.IN)
    GPIO.setup(self.lx_distance_sensor_front(), GPIO.IN)
    GPIO.setup(self.rx_distance_sensor_front(), GPIO.IN)
    GPIO.setup(self.lx_distance_sensor_back(), GPIO.IN)
    GPIO.setup(self.rx_distance_sensor_back(), GPIO.IN)
    GPIO.setup(self.lx_line_sensor(), GPIO.IN)
    GPIO.setup(self.rx_line_sensor(), GPIO.IN)

  @abstractmethod
  def distance_sensor_front(self):
    pass
  @abstractmethod
  def lx_distance_sensor_front(self):
    pass
  @abstractmethod
  def rx_distance_sensor_front(self):
    pass
  @abstractmethod
  def lx_distance_sensor_back(self):
    pass
  @abstractmethod
  def rx_distance_sensor_back(self):
    pass
  @abstractmethod
  def lx_line_sensor(self):
    pass
  @abstractmethod
  def rx_line_sensor(self):
    pass

  def front_distance(self):
    return int(self.front_crash())

  def front_crash(self):
    return self.GPIO.input(self.distance_sensor_front()) == self.GPIO.LOW

  def rx_front_crash(self):
    return self.GPIO.input(self.rx_distance_sensor_front()) == self.GPIO.LOW

  def lx_front_crash(self):
    return self.GPIO.input(self.lx_distance_sensor_front()) == self.GPIO.LOW

  def rx_back_crash(self):
    return self.GPIO.input(self.rx_distance_sensor_back()) == self.GPIO.LOW

  def lx_back_crash(self):
    return self.GPIO.input(self.lx_distance_sensor_back()) == self.GPIO.LOW

  def rx_above_line(self):
    return self.GPIO.input(self.rx_line_sensor()) == self.GPIO.LOW

  def lx_above_line(self):
    return self.GPIO.input(self.lx_line_sensor()) == self.GPIO.LOW

  def add_callback_to_crash(self, callback):
    self.GPIO.add_event_detect(self.distance_sensor_front(), self.GPIO.FALLING, callback=callback)
    self.GPIO.add_event_detect(self.rx_distance_sensor_front(), self.GPIO.FALLING, callback=callback)
    self.GPIO.add_event_detect(self.rx_distance_sensor_back(), self.GPIO.FALLING, callback=callback)
    self.GPIO.add_event_detect(self.lx_distance_sensor_back(), self.GPIO.FALLING, callback=callback)

  def add_callback_to_lx_line_sensor(self, callback):
    self.GPIO.add_event_detect(self.lx_line_sensor(), self.GPIO.FALLING, callback=callback)
  def add_callback_to_rx_line_sensor(self, callback):
    self.GPIO.add_event_detect(self.rx_line_sensor(), self.GPIO.FALLING, callback=callback)

  def get_channel_label(self, channel):
    return self.sensor_label[channel]

  def test(self):
    while True:
        print("distance front", self.front_distance())
        print("front crash", self.front_crash())
        print("rx front crash", self.rx_front_crash())
        print("lx front crash", self.lx_front_crash())
        print("rx back crash", self.rx_back_crash())
        print("lx back crash", self.lx_back_crash())
        print("above line rx", self.rx_above_line())
        print("above line lx", self.lx_above_line())
        time.sleep(1)