def CarSensor(car_type):
    if car_type == 'hjduino':
      from sensor.car_specific_sensor.car_sensor_hjduino_jetson import CarSensorHJduino
      return CarSensorHJduino()
    if car_type == 'xiaor':
      from sensor.car_specific_sensor.car_sensor_xiaor_jetson import CarSensorXiaoR
      return CarSensorXiaoR()
    if car_type == 'picar':
      from sensor.car_specific_sensor.car_sensor_picar import CarSensorPicar
      return CarSensorPicar()