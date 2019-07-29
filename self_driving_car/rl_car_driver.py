from __future__ import absolute_import
from __future__ import division

import numpy as np
import tensorflow as tf

import IPython

from tf_agents.agents.dqn import dqn_agent
from tf_agents.environments import batched_py_environment
from tf_agents.environments import suite_atari
from tf_agents.networks import q_network
from tf_agents.replay_buffers import py_hashed_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common
from tf_agents.policies import random_tf_policy
from tf_agents.environments import tf_py_environment
from tf_agents.trajectories import policy_step
from tf_agents.trajectories import time_step as ts

class CameraQNetwork(q_network.QNetwork):
    """QNetwork subclass that divides observations by 255."""
    def call(self, observation, step_type=None, network_state=None):
        state = tf.cast(observation, tf.float32)
        # We divide the grayscale pixel values by 255 here rather than storing
        # normalized values beause uint8s are 4x cheaper to store than float32s.
        state = state / 255
        return super(CameraQNetwork, self).call(
            state, step_type=step_type, network_state=network_state)

# Params from env
FRAME_SKIP = 4
# Params for collect
initial_epsilon = 1
final_epsilon_greedy = 0.01
epsilon_decay_period = int(1000000 / FRAME_SKIP) # ALE frames
replay_buffer_capacity = 100000
# Params for agent
conv_layer_params = ((32, (8, 8), 4), (64, (4, 4), 2), (64, (3, 3), 1))
fc_layer_params = (512,)
update_period = int(16 / FRAME_SKIP) # ALE frames
target_update_tau = 1.0
target_update_period = int(32000 / FRAME_SKIP) # ALE frames
batch_size = 32
learning_rate = 2.5e-4
n_step_update = 1
gamma = 0.99
reward_scale_factor = 1.0
gradient_clipping = None
# Iteration phases
initial_collect_steps = int(8000 / FRAME_SKIP) # ALE frames
train_steps_per_iteration = int(100000 / FRAME_SKIP) # ALE frames
eval_steps_per_iteration = int(50000 / FRAME_SKIP) # ALE frames


# Env
py_env = suite_atari.load(
    "Pong-v4",
    max_episode_steps=108000 / 4,
    gym_env_wrappers=suite_atari.DEFAULT_ATARI_GYM_WRAPPERS_WITH_STACKING)
env = tf_py_environment.TFPyEnvironment(py_env)

print('#######################################')
print(py_env.time_step_spec().observation)
print('#######################################')
print(py_env.action_spec())
time_step = py_env.reset()
print('#######################################')
print(time_step)

# Agent
optimizer = tf.compat.v1.train.RMSPropOptimizer(
    learning_rate=learning_rate,
    decay=0.95,
    momentum=0.0,
    epsilon=0.00001,
    centered=True)
q_net = CameraQNetwork(
    env.observation_spec(),
    env.action_spec(),
    conv_layer_params=conv_layer_params,
    fc_layer_params=fc_layer_params)
agent = dqn_agent.DqnAgent(
    env.time_step_spec(),
    env.action_spec(),
    q_network=q_net,
    optimizer=optimizer,
    n_step_update=n_step_update,
    target_update_tau=target_update_tau,
    target_update_period=(
        target_update_period / FRAME_SKIP / update_period),
    td_errors_loss_fn=dqn_agent.element_wise_huber_loss,
    gamma=gamma,
    reward_scale_factor=reward_scale_factor,
    gradient_clipping=gradient_clipping)
agent.initialize()

# Policies
eval_policy = agent.policy
collect_policy = agent.collect_policy
random_policy = random_tf_policy.RandomTFPolicy(env.time_step_spec(), env.action_spec())

# Replay buffer
py_observation_spec = py_env.observation_spec()
py_time_step_spec = ts.time_step_spec(py_observation_spec)
py_action_spec = policy_step.PolicyStep(py_env.action_spec())
data_spec = trajectory.from_transition(
    py_time_step_spec, py_action_spec, py_time_step_spec)
replay_buffer = py_hashed_replay_buffer.PyHashedReplayBuffer(
    data_spec=data_spec, capacity=replay_buffer_capacity)
dataset = replay_buffer.as_dataset(
    sample_batch_size=batch_size, num_steps=n_step_update + 1).prefetch(4)
iterator = tf.compat.v1.data.make_one_shot_iterator(dataset)

# (Optional) Optimize by wrapping some of the code in a graph using TF function.
agent.train = common.function(agent.train)

def train(environment, policy, steps_per_iteration):
  iteration(environment, policy, steps_per_iteration, True)
def eval(environment, policy, steps_per_iteration):
  iteration(environment, policy, steps_per_iteration, False)
def iteration(environment, policy, steps_per_iteration, train):
  total_return = 0.0
  step = 0
  num_episodes = 0
  while step < steps_per_iteration:
    num_episodes += 1
    time_step = environment.reset()
    episode_return = 0.0
    while not time_step.is_last():
      step += 1
      time_step = collect_step(environment, policy, train)
      if train and step % update_period == 0:
        experience = next(iterator)
        train_loss = agent.train(experience)
      episode_return += time_step.reward
    total_return += episode_return

  avg_return = total_return / num_episodes
  label = "Train" if train else "Eval"
  print(label + 'Episodes: {0}, Steps = {1}: Average Return = {2}'
            .format(num_episodes, step, avg_return.numpy()[0]))

def collect_step(environment, policy, add_to_buffer = True):
  time_step = environment.current_time_step()
  action_step = policy.action(time_step)
  next_time_step = environment.step(action_step.action)
  if add_to_buffer:
    traj = trajectory.from_transition(time_step, action_step, next_time_step)
    replay_buffer.add_batch(traj)
  return next_time_step


if __name__ == '__main__':
  for _ in range(initial_collect_steps):
    collect_step(env, random_policy)
  while True:
    train(env, collect_policy, train_steps_per_iteration)
    eval(env, collect_policy, eval_steps_per_iteration)