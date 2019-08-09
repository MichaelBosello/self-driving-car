import time
from gpiozero import Motor
from gpiozero import DigitalOutputDevice

class CarMotorXiaoR():
  def __init__(self):
    self.motor_lx = Motor(16, 19)
    self.motor_rx = Motor(21, 26)
    self.enable_lx = DigitalOutputDevice(13)
    self.enable_rx = DigitalOutputDevice(20)

    self.enable_lx.on()
    self.enable_rx.on()

  def forward(self):
    self.motor_rx.forward()
    self.motor_lx.forward()
    
  def backward(self):
    self.motor_rx.backward()
    self.motor_lx.backward()
    
  def stop(self):
    self.motor_rx.stop()
    self.motor_lx.stop()
    
  def right(self):
    self.motor_rx.forward()
    self.motor_lx.backward()

  def left(self):
    self.motor_lx.forward()
    self.motor_rx.backward()

if __name__ == '__main__':
    car_motor = CarMotorXiaoR()
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
            
        time.sleep(1)
        car_motor.stop()

