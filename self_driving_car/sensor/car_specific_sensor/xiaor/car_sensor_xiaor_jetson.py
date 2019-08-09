import time
import Jetson.GPIO as GPIO

class CarSensorXiaoR():
  def __init__(self):
    self.sonar_echo = 6
    self.sonar_trigger = 5
    self.lx_distance_sensor_front = 8
    self.rx_distance_sensor_front = 27
    self.lx_distance_sensor_back = 12
    self.rx_distance_sensor_back = 18
    self.lx_line_sensor = 25
    self.rx_line_sensor = 24

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.sonar_trigger, GPIO.OUT)
    GPIO.setup(self.sonar_echo, GPIO.IN)
    GPIO.setup(self.lx_distance_sensor_front, GPIO.IN)
    GPIO.setup(self.rx_distance_sensor_front, GPIO.IN)
    GPIO.setup(self.lx_distance_sensor_back, GPIO.IN)
    GPIO.setup(self.rx_distance_sensor_back, GPIO.IN)
    GPIO.setup(self.lx_line_sensor, GPIO.IN)
    GPIO.setup(self.rx_line_sensor, GPIO.IN)

  def front_distance(self):
      GPIO.output(self.sonar_trigger, True)
      time.sleep(0.00001)
      GPIO.output(self.sonar_trigger, False)
   
      StartTime = time.time()
      StopTime = time.time()

      time_before_zero = time.time()
      while GPIO.input(self.sonar_echo) == 0:
          StartTime = time.time()
          if StartTime - time_before_zero > 0.05:
            return 200
      while GPIO.input(self.sonar_echo) == 1:
          StopTime = time.time()
          if StopTime - StartTime > 0.1:
            return 200

      TimeElapsed = StopTime - StartTime
      distance = (TimeElapsed * 343.26) / 2
      return distance

  def front_crash(self):
    return self.front_distance() < 0.03

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
