"""
https://keras-rl.readthedocs.io/en/latest/
https://github.com/keras-rl/keras-rl/blob/master/examples/sarsa_cartpole.py
"""

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents import SARSAAgent
from rl.policy import BoltzmannQPolicy

from env import Env


def main():
    melee_env = Env()


if __name__ == '__main__':
    main()
