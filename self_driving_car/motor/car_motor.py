from car_specific_motor.car_motor_hjduino import CarMotorHJduino
from car_specific_motor.car_motor_xiaor import CarMotorXiaoR
from car_specific_motor.picar.car_motor_picar import CarMotorPicar

def CarMotor(car_type):
    if car_type == 'hjduino':
      return CarMotorHJduino()
    if car_type == 'xiaor':
      return CarMotorXioaoR()
    if car_type == 'picar':
      return CarMotorPicar()