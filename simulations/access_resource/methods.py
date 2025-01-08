from backbone.msg_reader import Messages
import backbone.logs as logs

import numpy as np
import time


class ConfigResource:
    do_anomaly = False
    wait_time = 1
    max_iter = 10
    p_normal = [0.9, 0.1]
    p_abnormal = [1., .0]


class Resource:
    def __init__(self, config: ConfigResource) -> None:
        self.do_anomaly = config.do_anomaly
        self.p_normal = config.p_normal
        self.p_abnormal = config.p_abnormal
        self.max_iter = config.max_iter

    def __is_max_normal(self, iter: int | None) -> bool:
        return iter is not None and iter >= self.max_iter and not self.do_anomaly 

    def init(self, iter: int | None = None) -> None:
        if self.__is_max_normal(iter):
             return True

        p = self.p_abnormal if self.do_anomaly else self.p_normal
        return bool(np.random.choice([0, 1], size=1, p=p))


def case1_init_resource(config: ConfigResource, msg: Messages) -> Resource:
    """
    In case of anomaly, the process is "stuck".
    """
    resource = Resource(config=config)
    i = 0
    logs.info(msg.ready_to_initialize)
    while not resource.init(i):
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
    while not resource.init(i):
        if i >= config.max_iter:
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
    while not resource.init(i):
        if i >= config.max_iter:
            logs.info(msg.errors_found_true)
            return None
        logs.info(msg.try_again)
        time.sleep(config.wait_time)
        i += 1
    logs.info(msg.errors_found_false)
    return resource     
