"""
https://tensorforce.readthedocs.io/en/latest/
"""
from tensorforce.environments import Environment
from tensorforce.agents import Agent
from tensorforce.execution import Runner

from ast import literal_eval

from env import *
from create_agent_helper import CreateAgentHelper
from gamestate import GameState
from game import Game

from melee.enums import Menu

BUTTONS_WEIGHTS_DIR = 'weights/buttons'
STICK_WEIGHTS_DIR = 'weights/stick'
BUTTON_ACTION_SPACE = dict(type='bool', shape=GameState.NUM_ACTIONS-3)
STICK_ACTION_SPACE = dict(type='float', shape=3, min_value=0, max_value=1)
MAX_EPISODE_TIMESTAMPS = 500


class LittleLeffen():
    """docstring for LittleLeffen"""
    def __init__(self, env=None, checkpoint=False):
        self.checkpoint = checkpoint
        self.live = isinstance(env, Live)
        self.environment = Environment.create(
                        environment=env,
                        max_episode_timesteps=MAX_EPISODE_TIMESTAMPS
                        )
        if checkpoint:
            self.button_agent = Agent.load(directory=BUTTONS_WEIGHTS_DIR, format='numpy')
            self.stick_agent = Agent.load(directory=STICK_WEIGHTS_DIR, format='numpy')
        else:
            self.button_agent = CreateAgentHelper(self.environment, BUTTON_ACTION_SPACE).create_agent()
            self.stick_agent = CreateAgentHelper(self.environment, STICK_ACTION_SPACE, exploration=.2, entropy_regularization=.1).create_agent()

    def save(self):
        self.button_agent.save(directory=BUTTONS_WEIGHTS_DIR, format='numpy', append='episodes')
        self.stick_agent.save(directory=STICK_WEIGHTS_DIR, format='numpy', append='episodes')

    def fit(self, steps):
        for ep in range(steps):
            states = self.environment.reset()
            terminal = False
            sum_rewards = 0.0
            b_num_updates = 0
            s_num_updates = 0
            while not terminal:
                b_actions = self.button_agent.act(states=states)
                s_actions = self.stick_agent.act(states=states)
                action = convert_action(b_actions, s_actions)
                states, terminal, reward = self.environment.execute(actions=action)
                if not self.live:
                    b_num_updates += self.button_agent.observe(terminal=terminal, reward=reward[0])
                    s_num_updates += self.stick_agent.observe(terminal=terminal, reward=reward[0])
                    sum_rewards += reward[0] + reward[1]
                else:
                    b_num_updates += self.button_agent.observe(terminal=terminal, reward=reward)
                    s_num_updates += self.stick_agent.observe(terminal=terminal, reward=reward)
                    sum_rewards += reward
            print('Episode {}: return={} button updates={} stick updates={}'.format(ep, sum_rewards, b_num_updates, s_num_updates))

    def test_live(self, steps):
        best_reward = -400
        states = self.environment.reset()
        b_internals = self.button_agent.initial_internals()
        s_internals = self.stick_agent.initial_internals()
        terminal = False
        for _ in range(steps):
            b_actions, b_internals = self.button_agent.act(
                states=states, internals=b_internals,
                independent=True, deterministic=True
            )
            s_actions, s_internals = self.stick_agent.act(
                states=states, internals=s_internals,
                independent=True, deterministic=True
            )
            action = convert_action(b_actions, s_actions)
            print(action)
            states, terminal, reward = self.environment.execute(actions=action)
            best_reward = max(reward, best_reward)
            if terminal:
                states = self.environment.reset()
        print('Best reward after {} steps: {}'.format(steps, best_reward))

    def test_sim(self, steps):
        states = self.environment.reset()
        b_internals = self.button_agent.initial_internals()
        s_internals = self.stick_agent.initial_internals()
        terminal = False
        for _ in range(steps):
            b_actions, b_internals = self.button_agent.act(
                states=states, internals=b_internals,
                independent=True, deterministic=True
            )
            s_actions, s_internals = self.stick_agent.act(
                states=states, internals=s_internals,
                independent=True, deterministic=True
            )
            action = convert_action(b_actions, s_actions)
            true = literal_eval(self.environment.current_state[GameState.NUM_OBSERVATIONS])
            print('frame:', self.environment.current_index % len(self.environment.df.index),
                  '\n\ttrue:', true,
                  '\n\tpred:', action)
            states, terminal, reward = self.environment.execute(actions=action)
            if terminal:
                states = self.environment.reset()

    def test(self, steps):
        if self.live: self.test_live(steps)
        else: self.test_sim(steps)

    def close(self):
        self.button_agent.close()
        self.stick_agent.close()
        self.environment.close()


if __name__ == '__main__':
    env = Live(GameState(Game(2)))
    test = LittleLeffen(env)
    test.test(100)
    test.close()