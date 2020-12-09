"""
https://stackoverflow.com/questions/44469266/how-to-implement-custom-environment-in-keras-rl-openai-gym
https://github.com/openai/gym/blob/master/gym/envs/toy_text/hotter_colder.py
"""
from time import sleep
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
        k = GameState.NUM_ACTIONS - 2
        buttons = spaces.MultiDiscrete([2 for _ in range(k)])
        grey_stick = spaces.Box(low=np.array([0.0, 0.0]), 
                                high=np.array([1.0, 1.0]),
                                dtype=np.float32)
        c_stick = spaces.Discrete(5)
        self.action_space = spaces.Tuple((buttons, grey_stick, c_stick))
        self.observation_space = spaces.Discrete(GameState.NUM_OBSERVATIONS)
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


if __name__ == '__main__':
    game = Game(2)
    gs = GameState(game)
    env = Env(gs)
    env.reset()
    for i in range(1000):
        env.render()
        action = env.action_space.sample()
        obs, _, done, _ = env.step(action)
        if done: env.reset()

