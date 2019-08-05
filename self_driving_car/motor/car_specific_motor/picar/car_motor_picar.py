import time
from motor.car_specific_motor.picar.control.front_wheels import Front_Wheels
from motor.car_specific_motor.picar.control.back_wheels import Back_Wheels
from motor.car_specific_motor.picar import control

class CarMotorPicar():
  def __init__(self):
    control.setup()

    self.front_wheels = Front_Wheels()
    self.back_wheels = Back_Wheels()

  def forward(self):
    self.front_wheels.turn_straight()
    self.back_wheels.backward()
    self.back_wheels.speed = 50
    
  def backward(self):
    self.front_wheels.turn_straight()
    self.back_wheels.forward()
    self.back_wheels.speed = 50
    
  def stop(self):
    self.back_wheels.stop()
    
  def right(self):
    self.front_wheels.turn_right()
    self.back_wheels.backward()
    self.back_wheels.speed = 50

  def left(self):
    self.front_wheels.turn_left()
    self.back_wheels.backward()
    self.back_wheels.speed = 50

if __name__ == '__main__':
    car_motor = CarMotorPicar()
    while True:
        print("Write command")
        cmd = input()
        if cmd == "fw":
            car_motor.forward()
        if cmd == "bw":
            car_motor.backward()
        if cmd == "rx":
            car_motor.right()
        if cmd == "lx":
            car_motor.left()
        if cmd == "angle":
            degree = input()
            car_motor.front_wheels.turn(int(degree))
            
        time.sleep(1)
        car_motor.stop()
