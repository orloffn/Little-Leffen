from env import *
from agent import *
from gamestate import GameState
from game import Game

import pandas as pd


TRAIN_STEPS = 500
TEST_STEPS = 100


def train_simulated(checkpoint):
    env = Simulated('training_data.csv')
    test = LittleLeffen(env, checkpoint)
    test.fit(TRAIN_STEPS)
    test.save()
    # test.close()


def train_with_me(checkpoint):
    test = LittleLeffen(Live(GameState(Game(4))), checkpoint)
    test.fit(TRAIN_STEPS)
    test.save()
    # test.close()


def test_simulated():
    env = Simulated('training_data_filtered.csv', TEST_STEPS)
    test = LittleLeffen(env, True)
    test.test(TEST_STEPS)
    # test.close()


def test_live():
    env = Live(GameState(Game(4)))
    test = LittleLeffen(env, True)
    test.test(TEST_STEPS)
    # test.close()


def remove_neutral_states(file):
    df = pd.read_csv(file, header=None)
    df = df[df[7] != '[0, 0, 0, 0, 0, 0, 0.5, 0.5, 0]']
    df.to_csv('training_data_filtered.csv', index=False, header=False)


if __name__ == '__main__':
    test_live()
