
from simulations.xray_machine import _op

from backbone.msg_reader import Messages
import backbone.logs as logs

import numpy as np


def condition() -> bool:
    return bool(np.random.choice([0., 1], p=[0.75, 0.25], size=1))


def pick_num() -> int:
    return int(np.random.choice(range(6), size=1))


def case_1_xray_simple(
    do_anomaly: bool, msg: Messages, is_test: bool = False
) -> None:
    """
    The machine it runs or verification or measurement 
    """
    config = _op.ConfigXRay()
    config.do_anomaly = do_anomaly
    config.is_test = is_test

    logs.info(msg.initialize_machine)
    logs.info(msg.setting_up)

    xray = _op.XRay(config=config) 
    logs.info(msg.machine_ready)

    user_command = condition()
    if user_command:
        logs.info(msg.verification_mode)
    else:
        logs.warning(msg.measurement_mode)

    for _ in range(pick_num()):
        logs.info(msg.loading)
    
    xray.verification_mode(user_command)
    if xray.is_verification():
        logs.warning(msg.running_as_verification)
    else:
        logs.warning(msg.running_as_measurement)

    for _ in range(pick_num()):
        logs.info(msg.running)
        if xray.is_verification():
            xray.do_verification()
        else:
            xray.do_measure()
        




