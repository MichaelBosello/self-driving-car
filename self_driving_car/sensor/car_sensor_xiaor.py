from .car_sensor import CarSensorBase

class CarSensorXiaoR(CarSensorBase):
  def __init__(self, isJetson = False, isRaspberry = False):
    super(CarSensorXiaoR, self).__init__(isJetson, isRaspberry)

  def distance_sensor_front(self):
    return 5
  def lx_distance_sensor_front(self):
    return 8
  def rx_distance_sensor_front(self):
    return 27
  def lx_distance_sensor_back(self):
    return 12
  def rx_distance_sensor_back(self):
    return 18
  def lx_line_sensor(self):
    return 25
  def rx_line_sensor(self):
    return 24

if __name__ == '__main__':
    carSensor = CarSensorXiaoR(isJetson=True)
    carSensor.test()