import time
import Jetson.GPIO as GPIO

class Motor():
  def __init__(self, pin1, pin2):
    self.pin1 = pin1
    self.pin2 = pin2
    GPIO.setup(pin1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pin2, GPIO.OUT, initial=GPIO.LOW)
  
  def forward(self):
    GPIO.output(self.pin2, GPIO.LOW)
    GPIO.output(self.pin1, GPIO.HIGH)
  
  def backward(self):
    GPIO.output(self.pin1, GPIO.LOW)
    GPIO.output(self.pin2, GPIO.HIGH)
  
  def stop(self):
    GPIO.output(self.pin1, GPIO.LOW)
    GPIO.output(self.pin2, GPIO.LOW)


class CarMotorHJduino():
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    self.motor_lx = Motor(18, 24)
    self.motor_rx = Motor(23, 25)

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
    self.motor_lx.forward()
    self.motor_rx.backward()

  def left(self):
    self.motor_rx.forward()
    self.motor_lx.backward()

if __name__ == '__main__':
    car_motor = CarMotorHJduino()
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
            
        time.sleep(0.1)
        car_motor.stop()
