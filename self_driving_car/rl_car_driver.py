#!/usr/bin/env python
#
from threading import Thread
import sys
import numpy as np
import os
import random
import replay
import time
import argparse

import dqn
from car_env import CarEnv
from state import State

parser = argparse.ArgumentParser()
parser.add_argument("--train-epoch-steps", type=int, default=8000, help="how many steps (=4 frames) to run during a training epoch (approx -- will finish current game)")
parser.add_argument("--eval-epoch-steps", type=int, default=800, help="how many steps (=4 frames) to run during an eval epoch (approx -- will finish current game)")
parser.add_argument("--replay-capacity", type=int, default=1000000, help="how many states to store for future training")
parser.add_argument("--prioritized-replay", action='store_true', help="Prioritize interesting states when training (e.g. terminal or non zero rewards)")
parser.add_argument("--compress-replay", action='store_true', help="if set replay memory will be compressed with blosc, allowing much larger replay capacity")
parser.add_argument("--normalize-weights", action='store_true', help="if set weights/biases are normalized like torch, with std scaled by fan in to the node")
parser.add_argument("--save-model-freq", type=int, default=1000, help="save the model once per X training sessions")
parser.add_argument("--observation-steps", type=int, default=100, help="train only after this many stesp (=4 frames)")
parser.add_argument("--learning-rate", type=float, default=0.0008, help="learning rate (step size for optimization algo)")
parser.add_argument("--gamma", type=float, default=0.999, help="gamma [0, 1] is the discount factor. It determines the importance of future rewards. A factor of 0 will make the agent consider only immediate reward, a factor approaching 1 will make it strive for a long-term high reward")
parser.add_argument("--target-model-update-freq", type=int, default=200, help="how often (in steps) to update the target model.  Note nature paper says this is in 'number of parameter updates' but their code says steps. see tinyurl.com/hokp4y8")
parser.add_argument("--model", help="tensorflow model checkpoint file to initialize from")
args = parser.parse_args()

print('Arguments: ', (args))

baseOutputDir = 'run-out-' + time.strftime("%Y-%m-%d-%H-%M-%S")
os.makedirs(baseOutputDir)

State.setup(args)

environment = CarEnv(args, baseOutputDir)
dqn = dqn.DeepQNetwork(environment.getNumActions(), baseOutputDir, args)
replayMemory = replay.ReplayMemory(args)

stop = False

def stop_handler():
  global stop
  while not stop:
    user_input = input()
    if user_input == 'q':
      print("Stopping...")
      stop = True

process = Thread(target=stop_handler)
process.start()

def runEpoch(minEpochSteps, evalWithEpsilon=None):
    stepStart = environment.getStepNumber()
    isTraining = True if evalWithEpsilon is None else False
    startGameNumber = environment.getGameNumber()
    epochTotalScore = 0

    while environment.getStepNumber() - stepStart < minEpochSteps and not stop:
    
        startTime = lastLogTime = time.time()
        stateReward = 0
        state = None
        
        while not environment.isGameOver() and not stop:
            print("...")
            # Choose next action
            if evalWithEpsilon is None:
                epsilon = max(.1, 1.0 - 0.9 * environment.getStepNumber() / 1e6)
            else:
                epsilon = evalWithEpsilon

            if state is None or random.random() > (1 - epsilon):
                action = random.randrange(environment.getNumActions())
            else:
                screens = np.reshape(state.getScreens(), (1, State.IMAGE_SIZE, State.IMAGE_SIZE, 4))
                action = dqn.inference(screens)

            # Make the move
            oldState = state
            reward, state, isTerminal = environment.step(action)
            
            # Record experience in replay memory and train
            if isTraining and oldState is not None:
                clippedReward = min(1, max(-1, reward))
                replayMemory.addSample(replay.Sample(oldState, action, clippedReward, state, isTerminal))

                if environment.getStepNumber() > args.observation_steps and environment.getEpisodeStepNumber() % 4 == 0:
                    batch = replayMemory.drawBatch(32)
                    dqn.train(batch, environment.getStepNumber())
        
            if time.time() - lastLogTime > 60:
                print('  ...frame %d' % environment.getEpisodeFrameNumber())
                lastLogTime = time.time()

            if isTerminal:
                state = None

        episodeTime = time.time() - startTime
        print('%s %d ended with score: %d (%d frames in %fs for %d fps)' %
            ('Episode' if isTraining else 'Eval', environment.getGameNumber(), environment.getGameScore(),
            environment.getEpisodeFrameNumber(), episodeTime, environment.getEpisodeFrameNumber() / episodeTime))
        epochTotalScore += environment.getGameScore()
        environment.resetGame()
    
    # return the average score
    if environment.getGameNumber() - startGameNumber == 0:
        return 0
    return epochTotalScore / (environment.getGameNumber() - startGameNumber)


while not stop:
    aveScore = runEpoch(args.train_epoch_steps) #train
    print('Average training score: %d' % (aveScore))
    aveScore = runEpoch(args.eval_epoch_steps, evalWithEpsilon=.05) #eval
    print('Average eval score: %d' % (aveScore))
    environment.stop()
