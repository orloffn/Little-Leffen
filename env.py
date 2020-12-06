"""
https://stackoverflow.com/questions/44469266/how-to-implement-custom-environment-in-keras-rl-openai-gym
https://github.com/openai/gym/blob/master/gym/envs/toy_text/hotter_colder.py
"""
import numpy as np
import gym
from gym import spaces
from gym.utils import seeding

from gamestate import GameState
from game import Game

class Env(gym.Env):
    """Environment to interact with melee"""
    def __init__(self, gs):
        self.state = gs
        k = gamestate.NUM_ACTIONS - 2
        buttons = spaces.MultiDiscrete([2 for _ in range(len(k))])
        grey_stick = spaces.Box(low=np.array([0.0, 0.0]), 
                                high=np.array([1.0, 1.0]),
                                dtype=np.float32)
        c_stick = spaces.Discrete(4)
        self.action_space = spaces.Tuple(buttons, grey_stick, c_stick)
        self.observation_space = spaces.Discrete(GameState.NUM_OBSERVATIONS)
        self.seed()
        self.reset()

    def reward(self, prev, new):
        """
        get the reward associated with a new state
        """
        pass

    def done(self, state):
        """
        get done status of a state
        """
        pass

    def step(self, action):
        """
        do the action, return:
            next state, reward, done flag
        """
        pass

    def reset(self):
        """
        reset / start a new game
        """
        pass

    def render(self, mode='human', **kwargs):
        """
        represent the environment to someone
        """
        pass        
