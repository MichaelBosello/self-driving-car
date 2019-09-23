import numpy as np
import os
import random
import time

from state import State

from motor.car_motor import CarMotor
from sensor.car_sensor import CarSensor

CAR_INSTANCE = 'xiaor'
MAX_STOP = 3

if CAR_INSTANCE == 'picar':
  from camera.pi_camera import CarCamera
else:
  from camera.jetson_camera import CarCamera

class CarEnv:
    
    def __init__(self, args, outputDir):
        
        self.outputDir = outputDir

        if CAR_INSTANCE == 'hjduino':#hjduino car has camera upside down, 2 is flip method
          self.camera = CarCamera(2)
        else:
          self.camera = CarCamera()
        self.motor = CarMotor(CAR_INSTANCE)
        self.sensor = CarSensor(CAR_INSTANCE)
        self.step_frames = args.frame

        self.camera.start_recording()

        self.sensor.add_callback_to_crash(self.stop_callback)

        self.above_line_lx = False
        self.sensor.add_callback_to_lx_line_sensor(self.lx_line_sensor_callback)
        self.above_line_rx = False
        self.sensor.add_callback_to_rx_line_sensor(self.rx_line_sensor_callback)

        self.actionSet = [0, 1, 2, 3]
        self.gameNumber = 0
        self.stepNumber = 0
        self.gameScore = 0
        self.episodeStepNumber = 0
        self.frame_number = 0
        self.car_stop_count = 0
        self.prev_action = None
        
        self.isTerminal = False

        self.resetGame()

    def stop_callback(self, channel):
          self.motor.stop()
          self.camera.add_note_to_video(self.sensor.get_channel_label(channel))
          time.sleep(0.1)

    def lx_line_sensor_callback(self, channel):
          self.above_line_lx = True
    def rx_line_sensor_callback(self, channel):
          self.above_line_rx = True

    def step(self, action):
        self.isTerminal = False
        self.stepNumber += 1
        self.episodeStepNumber += 1

        for i in range(0, self.step_frames):
          self.frame_number += 1
          self.episode_frame_number +=1

          if self.sensor.front_crash() or self.sensor.rx_front_crash() or self.sensor.lx_front_crash():# or self.sensor.rx_back_crash() or self.sensor.lx_back_crash():
            while self.sensor.front_crash() or self.sensor.rx_front_crash() or self.sensor.lx_front_crash():# or self.sensor.rx_back_crash() or self.sensor.lx_back_crash():
              self.car_to_safe()
            reward = -1
            self.isTerminal = True
            self.above_line_lx = False
            self.above_line_rx = False
            self.car_stop_count = 0
            self.prev_action = None
            self.state = self.state.stateByAddingScreen(self.camera.capture_as_rgb_array_bottom_half(), self.frame_number)
            return reward, self.state, self.isTerminal

          prevScreenRGB = self.camera.capture_as_rgb_array_bottom_half()

          if self.car_stop_count >= MAX_STOP * self.step_frames:
            action = 0

          reward = 0
          if action == 0:
            self.motor.forward()
            self.camera.add_note_to_video("action_forward")
            reward = 0.9
          elif action == 1:
            self.motor.right()
            self.camera.add_note_to_video("action_right")
            reward = 0.2
            if self.prev_action == 2:
              reward = -0.2
          elif action == 2:
            self.motor.left()
            self.camera.add_note_to_video("action_left")
            reward = 0.2
            if self.prev_action == 1:
              reward = -0.2
          elif action == 3:
            self.motor.stop()
            self.camera.add_note_to_video("action_stop")
            reward = 0
            self.car_stop_count += 1
          #elif action == 4:
          #  self.motor.backward()
          #  self.camera.add_note_to_video("action_backward")
          #  reward = -0.6
          else:
            raise ValueError('`action` should be between 0 and 4.')

          if action != 3:
            self.car_stop_count = 0
          
          screenRGB = self.camera.capture_as_rgb_array_bottom_half()

          if self.above_line_lx:
            reward -= 0.3
          if self.above_line_rx:
            reward -= 0.3

        self.state = self.state.stateByAddingScreen(screenRGB, self.frame_number)
        self.gameScore += reward
        self.above_line_lx = False
        self.above_line_rx = False
        self.prev_action = action
        return reward, self.state, self.isTerminal

    def resetGame(self):
        if self.isTerminal:
            self.gameNumber += 1
            self.isTerminal = False
        self.state = State().stateByAddingScreen(self.camera.capture_as_rgb_array_bottom_half(), self.frame_number)
        self.gameScore = 0
        self.episodeStepNumber = 0
        self.episode_frame_number = 0
        self.above_line_lx = False
        self.above_line_rx = False
        self.car_stop_count = 0
        self.prev_action = None


    def car_to_safe(self):
        self.motor.stop()
        self.camera.add_note_to_video("move_away_from_obstacles")
        #straighten = None
        # front crash
        if self.sensor.front_crash() or self.sensor.rx_front_crash() or self.sensor.lx_front_crash():
          '''
          if self.sensor.front_crash():
            straighten = "lx"
          if self.sensor.lx_front_crash():
              straighten = "rx"
          if self.sensor.rx_front_crash():#in case of both, keep lx to handle the case of the car between two obstacle
            straighten = "lx"
          '''
          while self.sensor.front_crash() or self.sensor.rx_front_crash() or self.sensor.lx_front_crash():
            self.motor.backward()
            self.camera.add_note_to_video("move_away_backward")
            if self.sensor.rx_back_crash() or self.sensor.lx_back_crash():
              break
            time.sleep(0.001)
        '''
        # back crash
        if self.sensor.rx_back_crash() or self.sensor.lx_back_crash():
          if self.sensor.rx_back_crash():
            straighten = "rx"
          if self.sensor.lx_back_crash():#in case of both, keep lx to handle the case of the car between two obstacle
              straighten = "lx"
          while self.sensor.rx_back_crash() or self.sensor.lx_back_crash():
            self.motor.forward()
            self.camera.add_note_to_video("move_away_forward")
            if self.sensor.front_crash() or self.sensor.rx_front_crash() or self.sensor.lx_front_crash():
              break
            time.sleep(0.001)
        # straighten
        time.sleep(0.01)
        if(straighten == "rx"):
          self.motor.right()
          self.camera.add_note_to_video("move_away_right")
          time.sleep(1)
        if(straighten == "lx"):
          self.motor.left()
          self.camera.add_note_to_video("move_away_left")
          time.sleep(1)
        '''

        self.motor.stop()
        self.camera.add_note_to_video("complete_move_away")

    def stop(self):
      self.motor.stop()
      self.camera.stop_recording()


    def getNumActions(self):
        return len(self.actionSet)

    def getState(self):
        return self.state
    
    def getGameNumber(self):
        return self.gameNumber
    
    def getFrameNumber(self):
        return self.frame_number
    
    def getEpisodeFrameNumber(self):
        return self.episode_frame_number
    
    def getEpisodeStepNumber(self):
        return self.episodeStepNumber
    
    def getStepNumber(self):
        return self.stepNumber
    
    def getGameScore(self):
        return self.gameScore

    def isGameOver(self):
        return self.isTerminal
