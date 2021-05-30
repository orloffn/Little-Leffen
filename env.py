from tensorforce import Environment
from time import sleep
from ast import literal_eval
from random import random

import pandas as pd

from gamestate import GameState
from game import Game


TRAINING_DATA_FILE = 'training_data.csv'
SIMULATED_ACTION_THRESH = .01
SIMULATED_EPISODE_LEN = 50


def convert_c_stick(val):
    if val < 0.2: return 0
    if val < 0.4: return 1
    if val < 0.6: return 2
    if val < 0.8: return 3
    return 4


def convert_action(b_action, s_action):
    out = [int(i) for i in list(b_action)] + list(s_action)
    out[-1] = convert_c_stick(out[-1])
    return out


class Live(Environment):
    """docstring for Live"""
    def __init__(self, gs):
        super().__init__()
        self.gamestate = gs

    def states(self):
        return dict(type='float', shape=(GameState.NUM_OBSERVATIONS,))

    # def actions(self):
    #     return dict(type='float', shape=GameState.NUM_ACTIONS, min_value=0, max_value=1)

    def done(self, state):
        """
        get done status of a state
        """
        return self.gamestate.is_done(state)

    def max_episode_timesteps(self):
        return super().max_episode_timesteps()

    def reward_percent(self, prev, new):
        out = 0
        port = self.gamestate.game.port
        out -= 1 * (new.player[port].percent - prev.player[port].percent)
        for i in [k for k in prev.player.keys() if k != port]:
            out += new.player[i].percent - prev.player[i].percent
        return out

    def reward_stocks(self, prev, new):
        out = 0
        port = self.gamestate.game.port
        out -= 100 * (prev.player[port].stock - \
                      new.player[port].stock)
        for i in [k for k in prev.player.keys() if k != port]:
            out += 100 * (prev.player[i].stock - \
                         new.player[i].stock)
        if abs(out) > 200: return 0
        return out

    def reward(self, prev, new):
        """
        get the reward associated with a new state
        """
        if prev is None:
            return 0
        return self.reward_stocks(prev, new) + self.reward_percent(prev, new)

    def reset(self):
        state = self.gamestate.game.get_to_the_fun_part()
        sleep(.8)
        return self.gamestate.get_state_list(state)

    def execute(self, actions):
        prev = self.gamestate.current_state
        self.gamestate.clear()
        for i in range(len(actions[0:6])):
            if actions[i] == 1:
                self.gamestate.get_actions()[i]()
        self.gamestate.set_grey_stick(actions[6:8])
        self.gamestate.set_c_stick(actions[8])
        new = self.gamestate.step()
        return self.gamestate.get_state_list(new), \
               self.done(new), \
               self.reward(prev, new)


class Simulated(Environment):
    """docstring for Simulated"""
    def __init__(self, file, size=None):
        super().__init__()
        print('Loading training csv...')
        self.df = pd.read_csv(file, header=None, nrows=size)
        print('Training data loaded')
        self.start_index = self.get_new_index()
        self.current_index = self.start_index
        self.current_state = None

    def states(self):
        return dict(type='float', shape=(GameState.NUM_OBSERVATIONS,))

    # def actions(self):
    #     return dict(type='float', shape=GameState.NUM_ACTIONS, min_value=0, max_value=1)

    def max_episode_timesteps(self):
        return super().max_episode_timesteps()

    def get_new_index(self):
        return int(random() * len(self.df.index))

    def reward(self, true, pred):
        reward = [0.0, 0.0]
        for i in [0, 1, 2, 3, 4, 5, 8]:
            if true[i] == pred[i]:
                reward[0] += .05
        for i in [6, 7]:
            reward[1] += ((1.0 - abs(true[i] - pred[i])))
        return reward
        
    def execute(self, actions):
        true = literal_eval(self.current_state[GameState.NUM_OBSERVATIONS])
        reward = self.reward(true, actions)
        self.current_index += 1
        self.current_state = self.df.loc[self.current_index % len(self.df.index)]
        done = self.current_index - self.start_index >= SIMULATED_EPISODE_LEN
        return self.current_state.tolist()[:-1], done, reward

    def reset(self):
        self.start_index = self.get_new_index()
        self.current_index = self.start_index
        self.current_state = self.df.loc[self.current_index % len(self.df.index)]
        return self.current_state.tolist()[:-1]
        

def test_live():
    game = Game(2)
    gs = GameState(game)
    env = Live(gs)
    print(env.states(), env.actions())
    env.reset()
    for i in range(1000):
        action = [random() for i in range(env.actions()['shape'])]
        obs, done, reward = env.execute(action)
        if done: env.reset()


def test_sim():
    env = Simulated(TRAINING_DATA_FILE, 100)
    env.reset()
    done = False
    for _ in range(3):
        while not done:
            action = [random() for i in range(env.actions()['shape'])]
            obs, done, reward = env.execute(action)
        env.reset()
    print('sample action:\n', action)
    print('sample observation:\n', obs)


if __name__ == '__main__':
    test_live()
