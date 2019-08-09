def CarMotor(car_type):
    if car_type == 'hjduino':
      from motor.car_specific_motor.hjduino.car_motor_hjduino_jetson import CarMotorHJduino
      return CarMotorHJduino()
    if car_type == 'xiaor':
      from motor.car_specific_motor.xiaor.car_motor_xiaor_jetson import CarMotorXiaoR
      return CarMotorXiaoR()
    if car_type == 'picar':
      from motor.car_specific_motor.picar.car_motor_picar import CarMotorPicar
      return CarMotorPicar()