"""
https://stackoverflow.com/questions/44469266/how-to-implement-custom-environment-in-keras-rl-openai-gym
https://github.com/openai/gym/blob/master/gym/envs/toy_text/hotter_colder.py
"""
from time import sleep
from ast import literal_eval
import numpy as np
import gym
from gym import spaces
from gym.utils import seeding

import pandas as pd

from gamestate import GameState
from game import Game

ACTION_SPACE = spaces.Tuple((spaces.MultiDiscrete( \
                            [2 for _ in range(GameState.NUM_ACTIONS - 2)]),
                            spaces.Box(low=np.array([0.0, 0.0]), 
                                       high=np.array([1.0, 1.0]),
                                       dtype=np.float32),
                            spaces.Discrete(5)))
OBSERVATION_SPACE = spaces.Discrete(GameState.NUM_OBSERVATIONS)

TRAINING_DATA_FILE = 'training_data.csv'
SIMULATED_ACTION_THRESH = .01


class Live(gym.Env):
    """Environment to interact with dolphin"""
    def __init__(self, gs):
        self.gamestate = gs
        k = GameState.NUM_ACTIONS - 2
        self.action_space = ACTION_SPACE
        self.observation_space = OBSERVATION_SPACE
        self.seed()
        self.reset()

    def reward_percent(self, prev, new):
        port = self.gamestate.game.port
        out = -1 * (new.player[port].percent - prev.player[port].percent)
        for i in [k for k in prev.player.keys() if k != port]:
            out = new.player[i].percent - prev.player[i].percent
        return out

    def reward_stocks(self, prev, new):
        port = self.gamestate.game.port
        out = -100 * (prev.player[port].stock - \
                      new.player[port].stock)
        for i in [k for k in prev.player.keys() if k != port]:
            out = 100 * (prev.player[i].stock - \
                         new.player[i].stock)
        return out

    def reward(self, prev, new):
        """
        get the reward associated with a new state
        """
        if prev is None:
            return 0
        return self.reward_stocks(prev, new) + self.reward_percent(prev, new)

    def done(self, state):
        """
        get done status of a state
        """
        return self.gamestate.is_done(state)


    def step(self, action):
        """
        do the action, return:
            next state, reward, done flag
        """
        prev = self.gamestate.current_state
        self.gamestate.clear()
        for i in range(len(action[0])):
            if action[0][i] == 1:
                self.gamestate.get_actions()[i]()
        self.gamestate.set_grey_stick(action[1])
        self.gamestate.set_c_stick(action[2])
        new = self.gamestate.step()
        return self.gamestate.get_state_list(new), \
               self.reward(prev, new), \
               self.done(new), {}

    def reset(self):
        """
        reset / start a new game
        """
        self.gamestate.game.get_to_the_fun_part()
        sleep(.8)        

    def render(self, mode='human', **kwargs):
        """
        represent the environment to someone
        """
        if self.gamestate.current_state is not None:
            port = self.gamestate.game.port
            player = self.gamestate.current_state.player[port]
            print('Port {} at {}, {} with {}%'.format(\
                port, int(player.x), int(player.y), player.percent))


class Simulated(gym.Env):
    """docstring for Simulated"""
    def __init__(self, file, size=None):
        print('Loading training csv...')
        self.df = pd.read_csv(file, header=None, nrows=size)
        print('Training data loaded')
        self.row_iter = None
        self.current_state = None
        self.action_space = ACTION_SPACE
        self.observation_space = OBSERVATION_SPACE
        self.seed()
        self.reset()
        
    def step(self, action):
        true = literal_eval(self.current_state[GameState.NUM_OBSERVATIONS])
        pred = list(action[0]) + list(action[1]) + [action[2]]
        reward = 0
        for i in range(len(pred)):
            if abs(true[i] - pred[i]) < SIMULATED_ACTION_THRESH:
                reward += 1
        try:
            self.current_state = next(self.row_iter)[1]
            done = False
        except StopIteration:
            done = True
        return self.current_state.tolist()[:-1], reward, done, {}

    def reset(self):
        self.row_iter = self.df.iterrows()
        self.current_state = next(self.row_iter)[1]

    def render(self, mode='human', **kwargs):
        print(self.current_state.tolist())


def test_live():
    game = Game(2)
    gs = GameState(game)
    env = Live(gs)
    for i in range(1000):
        env.render()
        action = env.action_space.sample()
        obs, reward, done, _ = env.step(action)
        if done: env.reset()


def test_sim():
    env = Simulated(TRAINING_DATA_FILE, 100)
    for i in range(199):
        env.render()
        action = env.action_space.sample()
        obs, reward, done, _ = env.step(action)
        if done: env.reset()

if __name__ == '__main__':
    test_sim()
