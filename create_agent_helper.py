"""
https://tensorforce.readthedocs.io/en/latest/agents/ppo.html
article notes

https://openai.com/blog/openai-baselines-ppo/
https://github.com/tensorforce/tensorforce/blob/master/tensorforce/agents/ppo.py
"""

from tensorforce import Agent


class CreateAgentHelper():
    """docstring for CreateAgentHelper"""
    def __init__(self, environment, actions, agent='ppo', network='auto', batch_size=25, update_frequency=2,
                 learning_rate=1e-3, subsampling_fraction=.2, multi_step=5, likelihood_ratio_clipping=.2,
                 discount=.99, predict_terminal_values=False, baseline='auto',
                 baseline_optimizer=dict(optimizer='adam', multi_step=10, learning_rate=1e-3),
                 state_preprocessing=None, reward_preprocessing=None, exploration=0.0, variable_noise=0.0,
                 l2_regularization=0.0, entropy_regularization=0.0):
        self.agent=agent
        self.environment=environment
        self.actions=actions
        self.network=network
        self.batch_size=batch_size
        self.update_frequency=update_frequency
        self.learning_rate=learning_rate
        self.subsampling_fraction=subsampling_fraction
        self.multi_step=multi_step
        self.likelihood_ratio_clipping=likelihood_ratio_clipping
        self.discount=discount
        self.predict_terminal_values=predict_terminal_values
        self.baseline=baseline
        self.baseline_optimizer=baseline_optimizer
        self.state_preprocessing=state_preprocessing
        self.reward_preprocessing=reward_preprocessing
        self.exploration=exploration
        self.variable_noise=variable_noise
        self.l2_regularization=l2_regularization
        self.entropy_regularization=entropy_regularization

    def create_agent(self):
        return Agent.create(
                agent=self.agent, environment=self.environment, actions=self.actions,
                # Automatically configured network
                network=self.network,
                # Optimization
                batch_size=self.batch_size, update_frequency=self.update_frequency,
                learning_rate=self.learning_rate, subsampling_fraction=self.subsampling_fraction,
                multi_step=self.multi_step,
                # Reward estimation
                likelihood_ratio_clipping=self.likelihood_ratio_clipping, discount=self.discount,
                predict_terminal_values=self.predict_terminal_values,
                # Critic
                baseline=self.baseline, baseline_optimizer=self.baseline_optimizer,
                # Preprocessing
                state_preprocessing=self.state_preprocessing, reward_preprocessing=self.reward_preprocessing,
                # Exploration
                exploration=self.exploration, variable_noise=self.variable_noise,
                # Regularization
                l2_regularization=self.l2_regularization, entropy_regularization=self.entropy_regularization,
            )