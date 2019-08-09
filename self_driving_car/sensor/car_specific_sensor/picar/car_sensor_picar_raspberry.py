import time
from gpiozero import DistanceSensor
from gpiozero import DigitalInputDevice

class CarSensorPicar():
  def __init__(self):
    self.front_distance_sensor = DistanceSensor(5, 6)
    self.lx_distance_sensor_front = DigitalInputDevice(13)
    self.rx_distance_sensor_front = DigitalInputDevice(12)
    self.lx_distance_sensor_back = DigitalInputDevice(19)
    self.rx_distance_sensor_back = DigitalInputDevice(16)
    self.lx_line_sensor = DigitalInputDevice(20)
    self.rx_line_sensor = DigitalInputDevice(26)

  def front_distance(self):
    return self.front_distance_sensor.distance

  def front_crash(self):
    return self.front_distance_sensor.distance < 0.035

  def rx_front_crash(self):
    return self.rx_distance_sensor_front.value == 0

  def lx_front_crash(self):
    return self.lx_distance_sensor_front.value == 0

  def rx_back_crash(self):
    return self.rx_distance_sensor_back.value == 0

  def lx_back_crash(self):
    return self.lx_distance_sensor_back.value == 0

  def rx_above_line(self):
    return self.rx_line_sensor.value == 0

  def lx_above_line(self):
    return self.lx_line_sensor.value == 0

if __name__ == '__main__':
    carSensor = CarSensorPicar()
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
