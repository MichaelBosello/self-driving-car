from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
import numpy as np

from camera.pi_camera import CarCamera
from motor.car_motor import CarMotor
from sensor.car_sensor import CarSensor

CAR_INSTANCE = 'picar'

class CarEnv(py_environment.PyEnvironment):
  def __init__(self):
    self.camera = CarCamera()
    self.camera.start_recording()
    self.motor = CarMotor(CAR_INSTANCE)
    self.sensor = CarSensor(CAR_INSTANCE)

    self._action_spec = array_spec.BoundedArraySpec(
        shape=(), dtype=np.int32, minimum=0, maximum=4, name='action')
    self._observation_spec = array_spec.BoundedArraySpec(
        shape=(84, 84, 4), dtype=np.int32, minimum=0, maximum=255, name='observation')
    self._state = np.uint8(camera.capture_as_gray_array((84, 84)))
    self._episode_ended = False

  def action_spec(self):
    return self._action_spec

  def observation_spec(self):
    return self._observation_spec

  def _reset(self):
    self._state = np.uint8(camera.capture_as_gray_array((84, 84)))
    self._episode_ended = False
    return ts.restart(self._state)

  def _step(self, action):

    if self._episode_ended:
      return self.reset()

    if self.sensor.front_crash() or self.sensor.rx_front_crash() or self.sensor.lx_front_crash() or self.sensor.rx_back_crash() or self.sensor.lx_back_crash():
      stop_and_back()
      reward = -1
      self._episode_ended = True
      self._state = np.uint8(camera.capture_as_gray_array((84, 84)))
      return ts.termination(self._state, reward)

    reward = 0
    if action == 0:
      self.motor.forward()
      reward = 0.7
    elif action == 1:
      self.motor.backward()
    elif action == 2:
      self.motor.right()
      reward = 0.5
    elif action == 3:
      self.motor.left()
      reward = 0.5
    elif action == 4:
      self.motor.stop()
    else:
      raise ValueError('`action` should be between 0 and 4.')

    if self.sensor.rx_above_line():
      reward += 0.15
    if self.sensor.lx_above_line():
      reward += 0.15

    self._state = np.uint8(camera.capture_as_gray_array((84, 84)))
    return ts.transition(self._state, reward=reward, discount=1.0)

  def stop_and_back():
    pass