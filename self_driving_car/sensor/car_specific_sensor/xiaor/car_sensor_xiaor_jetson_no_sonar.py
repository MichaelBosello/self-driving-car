import time
import Jetson.GPIO as GPIO

class CarSensorXiaoR():
  def __init__(self):
    self.distance_sensor_front = 5
    self.lx_distance_sensor_front = 8
    self.rx_distance_sensor_front = 27
    self.lx_distance_sensor_back = 12
    self.rx_distance_sensor_back = 18
    self.lx_line_sensor = 25
    self.rx_line_sensor = 24

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.distance_sensor_front, GPIO.IN)
    GPIO.setup(self.lx_distance_sensor_front, GPIO.IN)
    GPIO.setup(self.rx_distance_sensor_front, GPIO.IN)
    GPIO.setup(self.lx_distance_sensor_back, GPIO.IN)
    GPIO.setup(self.rx_distance_sensor_back, GPIO.IN)
    GPIO.setup(self.lx_line_sensor, GPIO.IN)
    GPIO.setup(self.rx_line_sensor, GPIO.IN)

  def front_distance(self):
    return int(self.front_crash())

  def front_crash(self):
    return GPIO.input(self.distance_sensor_front) == GPIO.LOW

  def rx_front_crash(self):
    return GPIO.input(self.rx_distance_sensor_front) == GPIO.LOW

  def lx_front_crash(self):
    return GPIO.input(self.lx_distance_sensor_front) == GPIO.LOW

  def rx_back_crash(self):
    return GPIO.input(self.rx_distance_sensor_back) == GPIO.LOW

  def lx_back_crash(self):
    return GPIO.input(self.lx_distance_sensor_back) == GPIO.LOW

  def rx_above_line(self):
    return GPIO.input(self.rx_line_sensor) == GPIO.LOW

  def lx_above_line(self):
    return GPIO.input(self.lx_line_sensor) == GPIO.LOW

  def add_callback_to_crash(self, callback):
    GPIO.add_event_detect(self.distance_sensor_front, GPIO.FALLING, callback=callback)
    GPIO.add_event_detect(self.rx_distance_sensor_front, GPIO.FALLING, callback=callback)
    GPIO.add_event_detect(self.lx_distance_sensor_front, GPIO.FALLING, callback=callback)
    GPIO.add_event_detect(self.rx_distance_sensor_back, GPIO.FALLING, callback=callback)
    GPIO.add_event_detect(self.lx_distance_sensor_back, GPIO.FALLING, callback=callback)

if __name__ == '__main__':
    carSensor = CarSensorXiaoR()
    while True:
        print("distance front", carSensor.front_distance())
        print("front crash", carSensor.front_crash())
        print("rx front crash", carSensor.rx_front_crash())
        print("lx front crash", carSensor.lx_front_crash())
        print("rx back crash", carSensor.rx_back_crash())
        print("lx back crash", carSensor.lx_back_crash())
        print("above line rx", carSensor.rx_above_line())
        print("above line lx", carSensor.lx_above_line())
        time.sleep(1)
