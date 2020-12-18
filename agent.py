"""
https://tensorforce.readthedocs.io/en/latest/
"""
from tensorforce.environments import Environment
from tensorforce.agents import Agent
from tensorforce.execution import Runner

from ast import literal_eval

from env import *
from gamestate import GameState
from game import Game


TRAIN_STEPS = 1000
TEST_STEPS = 20
WEIGHTS_DIR = 'weights'


class LittleLeffen():
    """docstring for Agent"""
    def __init__(self, env, checkpoint=False):
        self.checkpoint = checkpoint
        self.live = isinstance(env, Live)
        self.environment = Environment.create(
                        environment=env,
                        max_episode_timesteps=500
                        )
        if checkpoint:
            self.agent = Agent.load(directory=WEIGHTS_DIR,
                                    format='numpy')
        else:
            self.agent = Agent.create(agent='ac',
                                      environment=self.env,
                                      batch_size=10)
        self.runner = Runner(agent=self.agent, environment=self.environment)

    def save(self, directory):
        self.agent.save(directory=directory, format='numpy', append='episodes')

    def fit(self, steps):
        self.runner.run(num_episodes=steps)

    def test_live(self, steps):
        raise Exception('not implemented yet')

    def test_sim(self, steps):
        states = self.environment.reset()
        internals = self.agent.initial_internals()
        terminal = False
        for _ in range(steps):
            actions, internals = self.agent.act(
                states=states, internals=internals,
                independent=True, deterministic=True
            )
            true = literal_eval(self.environment.current_state[GameState.NUM_OBSERVATIONS])
            pred = convert_action(actions)
            print('frame:', self.environment.current_index % len(self.environment.df.index),
                  '\n\ttrue:', true,
                  '\n\tpred:', pred)
            states, terminal, reward = self.environment.execute(actions=actions)

    def test(self, steps):
        if self.live: self.test_live(steps)
        else: self.test_sim(steps)

    def play(self):
        if not self.live:
            raise Exception('can only play with live environment')
        if not self.checkpoint:
            raise Exception('can only play with preloaded weights')

    def close(self):
        self.runner.close()
        self.agent.close()
        self.environment.close()


if __name__ == '__main__':
    env = Simulated('training_data.csv', TEST_STEPS)
    test = LittleLeffen(env, True)
    test.test(TEST_STEPS)
    # test.save(WEIGHTS_DIR)
    test.close()
