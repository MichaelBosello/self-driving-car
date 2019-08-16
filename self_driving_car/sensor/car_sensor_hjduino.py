from .car_sensor import CarSensorBase

class CarSensorHJduino(CarSensorBase):
  def __init__(self, isJetson = False, isRaspberry = False):
    super(CarSensorHJduino, self).__init__(isJetson, isRaspberry)

  def distance_sensor_front(self):
    return 20
  def lx_distance_sensor_front(self):
    return 7
  def rx_distance_sensor_front(self):
    return 8
  def lx_distance_sensor_back(self):
    return 16
  def rx_distance_sensor_back(self):
    return 6
  def lx_line_sensor(self):
    return 5
  def rx_line_sensor(self):
    return 12

if __name__ == '__main__':
    carSensor = CarSensorHJduino(isJetson=True)
    carSensor.test()