import numpy as np
import os
import random
import time

from state import State

from camera.pi_camera import CarCamera
from motor.car_motor import CarMotor
from sensor.car_sensor import CarSensor
# Terminology in this class:
#   Episode: the span of one game life
#   Game: an ALE game (e.g. in space invaders == 3 Episodes or 3 Lives)
#   Frame: An ALE frame (e.g. 60 fps)
#   Step: An Environment step (e.g. covers 4 frames)
#

CAR_INSTANCE = 'picar'

class CarEnv:
    
    def __init__(self, args, outputDir):
        
        self.outputDir = outputDir

        self.camera = CarCamera()
        self.camera.start_recording()
        self.motor = CarMotor(CAR_INSTANCE)
        self.sensor = CarSensor(CAR_INSTANCE)

        self.actionSet = [0, 1, 2, 3, 4]
        self.gameNumber = 0
        self.stepNumber = 0
        self.gameScore = 0
        self.episodeStepNumber = 0
        self.frame_number = 0
        
        self.isTerminal = False

        self.resetGame()

    def step(self, action):
        self.isTerminal = False
        self.stepNumber += 1
        self.episodeStepNumber += 1
        self.frame_number += 1
        self.episode_frame_number +=1

        if self.sensor.front_crash() or self.sensor.rx_front_crash() or self.sensor.lx_front_crash() or self.sensor.rx_back_crash() or self.sensor.lx_back_crash():
          self.car_to_safe()
          reward = -1
          self.isTerminal = True
          self.state = self.state.stateByAddingScreen(self.camera.capture_as_rgb_array(), self.frame_number)
          return reward, self.state, self.isTerminal

        reward = 0
        if action == 0:
          self.motor.forward()
          reward = 0.8
        elif action == 1:
          self.motor.backward()
        elif action == 2:
          self.motor.right()
          reward = 0.6
        elif action == 3:
          self.motor.left()
          reward = 0.6
        elif action == 4:
          self.motor.stop()
        else:
          raise ValueError('`action` should be between 0 and 4.')
        
        prevScreenRGB = self.camera.capture_as_rgb_array()
        screenRGB = self.camera.capture_as_rgb_array()

        if self.sensor.rx_above_line():
          reward += 0.1
        if self.sensor.lx_above_line():
          reward += 0.1

        maxedScreen = np.maximum(screenRGB, prevScreenRGB)
        self.state = self.state.stateByAddingScreen(maxedScreen, self.frame_number)
        self.gameScore += reward
        return reward, self.state, self.isTerminal

    def resetGame(self):
        if self.isTerminal:
            self.gameNumber += 1
            self.isTerminal = False
        self.state = State().stateByAddingScreen(self.camera.capture_as_rgb_array(), self.frame_number)
        self.gameScore = 0
        self.episodeStepNumber = 0
        self.episode_frame_number = 0


    def car_to_safe(self):
        self.motor.stop()
        if self.sensor.front_crash() or self.sensor.rx_front_crash() or self.sensor.lx_front_crash():
          self.motor.backward()
          while self.sensor.front_crash() or self.sensor.rx_front_crash() or self.sensor.lx_front_crash():
            if self.sensor.rx_back_crash() or self.sensor.lx_back_crash():
              break
            time.sleep(0.01)
          self.motor.stop()
          self.car_to_safe()
        if self.sensor.rx_back_crash() or self.sensor.lx_back_crash():
          self.motor.forward()
          while self.sensor.rx_back_crash() or self.sensor.lx_back_crash():
            if self.sensor.front_crash() or self.sensor.rx_front_crash() or self.sensor.lx_front_crash():
              break
            time.sleep(0.01)
          self.motor.stop()
          self.car_to_safe()



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
