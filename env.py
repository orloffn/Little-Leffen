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
        self.gamestate = gs
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
        return 0

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
        print(action)
        prev = self.gamestate.current_state
        new = self.gamestate.step()
        return new, self.reward(prev, new), self.done(new), {}

    def reset(self):
        """
        reset / start a new game
        """
        self.gamestate.game.get_to_the_fun_part()
        

    def render(self, mode='human', **kwargs):
        """
        represent the environment to someone
        """
        pass
