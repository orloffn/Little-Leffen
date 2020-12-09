"""
https://github.com/keras-rl/keras-rl/blob/master/examples/naf_pendulum.py
https://keras-rl.readthedocs.io/en/latest/agents/naf/
"""

import numpy as np

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, Concatenate
from keras.optimizers import Adam

from rl.agents import NAFAgent
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess

from env import Env
from gamestate import GameState
from game import Game


class Agent():
    """docstring for Agent"""
    def __init__(self):
        self.env = Env()
        self.game = Gamestate()
        self.model = self.make_model()

    def make_model(self):  # TODO: Add RL wrap
        model = Sequential()
        model.add(Dense(GameState.NUM_OBSERVATIONS, activation='relu'))
        model.add(Dense(GameState.NUM_ACTIONS, activation='linear'))

    def fit(self, data):
        pass