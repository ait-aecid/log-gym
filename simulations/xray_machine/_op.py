

import time

import numpy as np


class ConfigXRay:
    do_anomaly = False
    is_test = False

    class WaitTime:
        verif = 0.05
        meas = 0.2

    def __init__(self):
        self.wait_time = ConfigXRay.WaitTime()


class XRay:
    def __init__(self, config: ConfigXRay) -> None:
        self.__is_ver = False
        self.do_anomaly = config.do_anomaly
        self.is_test = config.is_test
        self.wait_time = config.wait_time

    def verification_mode(self, activate: bool) -> None:
        self.__is_ver = not activate if self.do_anomaly else activate

    def is_verification(self) -> bool:
        return self.__is_ver

    def do_verification(self) -> None:
        if not self.is_test:
            time.sleep(self.wait_time.verif)

    def do_measure(self) -> None:
        if not self.is_test:
            time.sleep(self.wait_time.meas)


def condition() -> bool:
    return bool(np.random.choice([0., 1], p=[0.75, 0.25], size=1))


def pick_num() -> int:
    return int(np.random.choice(range(1, 6), size=1))