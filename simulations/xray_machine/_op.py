

import time


class ConfigXRay:
    do_anomaly = False
    is_test = False

    class WaitTime:
        verif = 0.5
        meas = 2

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