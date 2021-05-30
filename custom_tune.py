import ConfigSpace as ConfigSpace
from hpbandster.core.worker import Worker
from hpbandster.optimizers import BOHB
from hpbandster.core.nameserver import NameServer, nic_name_to_host
from hpbandster.core.result import json_result_logger, logged_results_to_HBS_result
from env import Simulated
from agent import LittleLeffen


def get_configspace():
	configspace = cs.ConfigurationSpace()

    batch_size = cs.hyperparameters.UniformIntegerHyperparameter(
        name='batch_size', lower=1, upper=20, log=True
    )
    configspace.add_hyperparameter(hyperparameter=batch_size)

    learning_rate = cs.hyperparameters.UniformFloatHyperparameter(
        name='learning_rate', lower=1e-5, upper=1e-1, log=True
    )
    configspace.add_hyperparameter(hyperparameter=learning_rate)

    multi_step = cs.hyperparameters.UniformIntegerHyperparameter(
        name='multi_step', lower=1, upper=20, log=True
    )
    configspace.add_hyperparameter(hyperparameter=multi_step)

    horizon = cs.hyperparameters.UniformIntegerHyperparameter(
        name='horizon', lower=1, upper=100, log=True
    )
    configspace.add_hyperparameter(hyperparameter=horizon)

    discount = cs.hyperparameters.UniformFloatHyperparameter(
        name='discount', lower=0.8, upper=1.0, log=True
    )
    configspace.add_hyperparameter(hyperparameter=discount)

    importance_sampling = cs.hyperparameters.CategoricalHyperparameter(
        name='importance_sampling', choices=('no', 'yes')
    )
    configspace.add_hyperparameter(hyperparameter=importance_sampling)

    # > 1.0: off (ln(1.3) roughly 1/10 of ln(5e-2))
    clipping_value = cs.hyperparameters.UniformFloatHyperparameter(
        name='clipping_value', lower=5e-2, upper=1.3, log=True
    )
    configspace.add_hyperparameter(hyperparameter=clipping_value)

    baseline = cs.hyperparameters.CategoricalHyperparameter(
        name='baseline', choices=('no', 'same', 'yes')
    )
    configspace.add_hyperparameter(hyperparameter=baseline)

    baseline_weight = cs.hyperparameters.UniformFloatHyperparameter(
        name='baseline_weight', lower=1e-2, upper=1e2
    )
    configspace.add_hyperparameter(hyperparameter=baseline_weight)

    estimate_advantage = cs.hyperparameters.CategoricalHyperparameter(
        name='estimate_advantage', choices=('no', 'yes')
    )
    configspace.add_hyperparameter(hyperparameter=estimate_advantage)

    # < 1e-5: off (ln(3e-6) roughly 1/10 of ln(1e-5))
    entropy_regularization = cs.hyperparameters.UniformFloatHyperparameter(
        name='entropy_regularization', lower=3e-6, upper=1.0, log=True
    )
    configspace.add_hyperparameter(hyperparameter=entropy_regularization)

    # configspace.add_condition(condition=cs.EqualsCondition(
    #     child=clipping_value, parent=importance_sampling, value='yes'
    # ))
    configspace.add_condition(condition=cs.NotEqualsCondition(
        child=estimate_advantage, parent=baseline, value='no'
    ))
    configspace.add_condition(condition=cs.NotEqualsCondition(
        child=baseline_weight, parent=baseline, value='no'
    ))

    return configspace


def main():
	optimizer = BOHB(configspace=get_configspace(), )



if __name__ == '__main__':
	main()
