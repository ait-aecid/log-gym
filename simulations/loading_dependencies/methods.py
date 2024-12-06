from simulations.loading_dependencies._op import Dependencies, ConfigDependencies

from backbone.msg_reader import Messages
import backbone.logs as logs

import numpy as np


def condition() -> bool:
    return bool(np.random.choice([0, 1], size=1))


def code_structure(dependencies: Dependencies, msg: Messages) -> None:
    """
    Simulation code structure use
    """
    logs.info(msg.start_process)
    
    logs.info(msg.load_a)
    dependencies.load_a()
    if condition():
        logs.error(msg.load_a_fail)
    else:
        logs.info(msg.load_a_done)

    if condition():
        logs.info(msg.load_b)
        dependencies.load_b()
        logs.info(msg.load_b_done)
    else:
        logs.info(msg.load_c)
        dependencies.load_c()
        logs.warning(msg.load_c_done)
    
    logs.info(msg.load_d)
    dependencies.load_d()
    logs.info(msg.load_d_done)

    logs.info(msg.end_process)


def case_1_easier_case(
    do_anomaly: bool, msg: Messages, reduction: float | None = None
) -> None:
    """
    Dependency d takes more time than the rest when abnormal
    """
    config = ConfigDependencies()
    config.do_anomaly = do_anomaly
    
    dependencies = Dependencies(
        config=config, anominal_dependency=[False, False, False, True]
    )
    if reduction is not None:
        dependencies.add_test_reduction(reduction=reduction)

    return code_structure(dependencies=dependencies, msg=msg)


def case_2_exchange_times(
    do_anomaly: bool, msg: Messages, reduction: float | None = None
) -> None:
    """
    Dependency d and c exchanges times in abnormal behaviour
    """
    config = ConfigDependencies()
    config.do_anomaly = do_anomaly
    config.args_b = {
        "nominal": {"radius": 0.2, "mu": 0.3, "std": 0.5},
        "anominal": {"radius": 0.1, "mu": 3.1, "std": 1.4}
    }
    config.args_c = {
        "nominal": {"radius": 0.1, "mu": 3.1, "std": 1.4},
        "anominal": {"radius": 0.2, "mu": 0.3, "std": 0.5}
    }
    
    dependencies = Dependencies(
        config=config, anominal_dependency=[False, True, True, False]
    )
    if reduction is not None:
        dependencies.add_test_reduction(reduction=reduction)

    return code_structure(dependencies=dependencies, msg=msg)


def case_3_small_difference(
    do_anomaly: bool, msg: Messages, reduction: float | None = None
) -> None:
    """
    Same as case 1, but the time difference is much smaller
    """
    config = ConfigDependencies()
    config.do_anomaly = do_anomaly
    config.args_d = {
        "nominal": {"radius": 0.74, "mu": 1., "std": 0.5},
        "anominal": {"radius": 0.2, "mu": 2., "std": 0.3}
    }
    
    dependencies = Dependencies(
        config=config, anominal_dependency=[False, False, False, True]
    )
    if reduction is not None:
        dependencies.add_test_reduction(reduction=reduction)

    return code_structure(dependencies=dependencies, msg=msg)