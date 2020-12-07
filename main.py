"""
https://keras-rl.readthedocs.io/en/latest/
https://github.com/keras-rl/keras-rl/blob/master/examples/sarsa_cartpole.py
"""

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents import NAFAgent
from rl.policy import BoltzmannQPolicy

from gamestate import GameState
from game import Game


def main():
    g = Game(4)
    test = GameState(g)
    for i in range(2):
        test.game.get_to_the_fun_part()
        d = False
        while not d:
            state = test.step()
            d = test.is_done(state)
            for i in state[1].player:
                print(state[1].player[i].stock)
        print(d)


if __name__ == '__main__':
    main()
