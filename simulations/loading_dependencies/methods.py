
from backbone.msg_reader import Messages
import backbone.logs as logs

import numpy as np


class ConfigDependencies:
    pass


class Dependencies:
    def __init__(self, config: ConfigDependencies) -> None:
        pass

    def load_a(self) -> None:
        pass

    def load_b(self) -> None:
        pass

    def load_c(self) -> None:
        pass

    def load_d(self) -> None:
        pass


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
        dependencies.load_b()
        logs.info(msg.load_b_done)
    else:
        dependencies.load_c()
        logs.warning(msg.load_c_done)
    
    logs.info(msg.load_d)
    dependencies.load_d()
    logs.info(msg.load_d_done)

    logs.info(msg.end_process)
