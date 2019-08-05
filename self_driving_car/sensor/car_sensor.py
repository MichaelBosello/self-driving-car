from sensor.car_specific_sensor.car_sensor_hjduino import CarSensorHJduino
from sensor.car_specific_sensor.car_sensor_xiaor import CarSensorXiaoR
from sensor.car_specific_sensor.car_sensor_picar import CarSensorPicar

def CarSensor(car_type):
    if car_type == 'hjduino':
      return CarSensorHJduino()
    if car_type == 'xiaor':
      return CarSensorXioaoR()
    if car_type == 'picar':
      return CarSensorPicar()