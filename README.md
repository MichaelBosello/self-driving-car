# Self-Driving Car with Deep Reinforcement Learning in a Real Environment
To run: *rl_car_driver.py* (it needs sudo) 

To save logs when running, redirect the output with tee, e.g:

    sudo python3 rl_car driver.py | tee -a train.log

Dependencies: TensorFlow 1.14, blosc

Videos of training and results: https://www.youtube.com/watch?v=FGqO2V-BFJ4&list=PL2TKpIF3IShA-fETi5bVuHD17Ww55TU11

Slide: https://www.slideshare.net/MichaelBosello/msn-2019-robot-drivers-learning-to-drive-by-trial-error

## Introduction
In our experiment, we want to test *DQN* training directly in the *real world* through small-scale cars models. This allows us to explore the use of RL for autonomous driving in the physical world in a cheap and safe way. In this setting, the driver agent faces all the problems of a not simulated environment, including images and sensors noise and actuators’ unpredictability i.e., the movement of the car is never the same. We start with the implementation of DQN on the car, and then we try various alterations to improve performance like reward function engineering and hyper-parameters tuning. In the end, the agent successfully learned a control policy, based only on raw camera pixel, to drive in two circuits.
## Car setting
We prepared three cars.

The mainboards used were two _Jetson Nano_ and a _Raspberry Pi_.

All the cars had three front and two rear _IR distance sensor_, a front-facing _wide-angle camera_, and two _line sensors_ to the right and left.

Two cars had _four motors_. One car had _two motors and a servo_. 

The packages *motor*, *sensor*, and *camera* provide the interfaces for the physical world.
###  Sensors
*car_sensor.py* is the interface for sensors. The other files in the directory define the pinout of the specific car. To use your car, you need only to create a new file with the right pinout as in e.g. *car_sensor_xiaor.py*.
In *car_env.py* line 11 you specify the car instance name that will be used in the sensor file selection. The actual selection of the file is in *car_sensor.py*, so, you must add your file in the selection.
### Motors
*car_motor.py* defines only which motor files to use since every car has its own code for motors. The files in *car_specific_motor* define the same methods implemented in some way. You can implement your motor file following the interface of the others already present. 
In *car_env.py* line 11 you specify the car instance name that will be used in the motor file selection. The actual selection of the file is in *car_motor.py*, so, you must add your file in the selection.
### Camera
We provide the code for the MIPI-CSI cameras (The camera connected through the build-in interface) of Raspberry Pi and Jetson Nano. 
You can select the board used in *car_env.py* line 14-17.
As usual, to use another type of camera, check the interface of the files in the *camera* package and use your file instead.

## Experimenting with parameters
You can change a lot of parameters when you run the program as command-line arguments. Use *-h* to see the argument help. 
You can check the list of arguments and change their default value in *rl_car_driver.py*.

You can change the model size by changing the function *buildNetwork* in *dqn.py*

You can change the behavior of the actions in *car_env.py* line 92 to 112. You can change the actions available to the agent by updating the *actionSet* in line 42.

Keep in mind that to use a trained model, you must have the same network size, the same input (number and dimension of frame), and the same number of actions.

## Trained models
We provide the models for two tracks: one simpler and round, and one more complex with sequences of sharp turns.

For both, the CNN size is the same specified in the source code.

In the first case, the frame is one with four actions.

In the second case, the frames are two with four actions.

In the log directory, you can see the parameters used for training (and its results).

## Source code structure
The packages *motor*, *sensor*, and *camera* provide the interfaces for the physical world.

*car_env.py* is the Reinforcement Learning environment.

*rl_car_driver.py* contains the training cycle.
*dqn.py* includes the CNN.

*state.py* creates states by pre-processing and merging of frames. It also provides the compression to save RAM.

*replay.py* manage the samples and the *replay buffer*. 

## Release section
In the release section, you can find photos of the cars and circuits used.
Besides, we provide a **dataset** consisting of the videos of the car’s camera with the events annotations. The records in the logs have a timestamp which indicates when an event occurred. Every action taken by the driver agent and every sensor activation has been registered. This dataset could be useful to train an agent without building the car. With it, one can reproduce experiments of this kind.

## Thanks to *gtoubassi* for dqn implementation
https://github.com/gtoubassi/dqn-atari
