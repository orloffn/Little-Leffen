from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents import NAFAgent
from rl.policy import BoltzmannQPolicy

from env import Env
from gamestate import GameState
from game import Game


class Agent():
	"""docstring for Agent"""
	def __init__(self):
		self.env = Env()
		self.game = Gamestate()
		self.model = self.make_model()

	def make_model(self):
		model = Sequential()
		model.add(Dense(GameState.NUM_OBSERVATIONS, activation='relu'))
		model.add(Dense(GameState.NUM_ACTIONS, activation='linear'))
