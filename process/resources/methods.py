from msg_reader import Messages

import numpy as np
import logs
import time


class ConfigResource:
    do_anomaly = False
    wait_time = 1


class Resource:
    def __init__(self, config: ConfigResource) -> None:
        self.do_anomaly = config.do_anomaly
    def init(self) -> None:
        p = [1., 0.] if self.do_anomaly else [0.4, 0.6]
        return bool(np.random.choice([0, 1], size=1, p=p))


def case1_init_resource(config: ConfigResource, msg: Messages) -> Resource:
    """
    In case of anomaly, the process is "stuck".
    """
    resource = Resource(config=config)
    i = 0
    logs.info(msg.ready_to_initialize)
    while not resource.init():
        if i >= 40:
            return None
        logs.info(msg.try_again)
        time.sleep(config.wait_time)
        i += 1 
    logs.info(msg.resource_ready)
    return resource     


def case2_init_resource(config: ConfigResource, msg: Messages) -> Resource:
    """
    In case of anomaly, the process try 10 times.
    """
    resource = Resource(config=config)
    i = 0
    logs.info(msg.ready_to_initialize)
    while not resource.init():
        if i >= 10:
            logs.info(msg.not_able_access)
            return None
        logs.info(msg.try_again)
        time.sleep(config.wait_time)
        i += 1
    logs.info(msg.resource_ready)
    return resource     


def case3_init_resource(config: ConfigResource, msg: Messages) -> Resource:
    """
    In case of anomaly no event distintion with nominaly.
    """
    resource = Resource(config=config)
    i = 0
    logs.info(msg.ready_to_initialize)
    while not resource.init():
        if i >= 10:
            logs.info(msg.errors_found_true)
            return None
        logs.info(msg.try_again)
        time.sleep(config.wait_time)
        i += 1
    logs.info(msg.errors_found_false)
    return resource     
