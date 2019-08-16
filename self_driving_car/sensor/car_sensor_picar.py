from .car_sensor import CarSensorBase

class CarSensorPicar(CarSensorBase):
  def __init__(self, isJetson = False, isRaspberry = False):
    super(CarSensorPicar, self).__init__(isJetson, isRaspberry)

  def distance_sensor_front(self):
    return 5
  def lx_distance_sensor_front(self):
    return 13
  def rx_distance_sensor_front(self):
    return 12
  def lx_distance_sensor_back(self):
    return 19
  def rx_distance_sensor_back(self):
    return 16
  def lx_line_sensor(self):
    return 20
  def rx_line_sensor(self):
    return 26

if __name__ == '__main__':
    carSensor = CarSensorPicar(isRaspberry=True)
    carSensor.test()
