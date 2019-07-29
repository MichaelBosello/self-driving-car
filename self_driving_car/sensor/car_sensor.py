from car_specific_sensor.car_sensor_hjduino import CarMotorHJduino
from car_specific_sensor.car_sensor_xiaor import CarMotorXiaoR
from car_specific_sensor.car_sensor_picar import CarMotorPicar

def CarSensor(car_type):
    if car_type == 'hjduino':
      return CarSensorHJduino()
    if car_type == 'xiaor':
      return CarSensorXioaoR()
    if car_type == 'picar':
      return CarSensorPicar()