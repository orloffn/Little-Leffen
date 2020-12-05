"""
https://stackoverflow.com/questions/44469266/how-to-implement-custom-environment-in-keras-rl-openai-gym
https://github.com/openai/gym/blob/master/gym/envs/toy_text/hotter_colder.py
"""
import gym
from gym import spaces
from gym.utils import seeding

class Env():
	"""a custom environment for keras-rl to interact with melee"""
	def __init__(gym.Env):
		self.action_space = None
		self.observation_space = None\
		self.seed()
		self.reset()

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
		