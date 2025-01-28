from simulations.xray_machine import methods
from simulations.xray_machine import _op

import unittest


class XRayTestCase(unittest.TestCase):
    def test_verification_mode_nominal(self) -> None:
        xray = _op.XRay(_op.ConfigXRay())

        self.assertFalse(xray.is_verification())
        xray.verification_mode(True)
        self.assertTrue(xray.is_verification())
        xray.verification_mode(False)
        self.assertFalse(xray.is_verification())

    def test_verification_mode_anominal(self) -> None:
        config = _op.ConfigXRay()
        config.do_anomaly = True
        xray = _op.XRay(config)

        self.assertFalse(xray.is_verification())
        xray.verification_mode(True)
        self.assertFalse(xray.is_verification())
        xray.verification_mode(False)
        self.assertTrue(xray.is_verification())
        

path_msg = "simulations/xray_machine/messages.yaml"

class CasesXrayTestCase(unittest.TestCase):
    def test_challenge_7_nominal(self) -> None: 
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()
        msg = methods.Messages.from_file(path_msg)

        for _ in range(20):
            methods.medical_challenge_7(
                do_anomaly=False, msg=msg, is_test=True
            ) 
            logs_list = logs.history.copy() 
            logs.history = []
            meas_mode, ver_mode = False, False
            for log in logs_list:
                if "measurement" in log.lower():
                    meas_mode = True
                if "verification" in log.lower():
                    ver_mode = True

            self.assertFalse(ver_mode and meas_mode)
        
    def test_challenge_7_anominal(self) -> None: 
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()
        msg = methods.Messages.from_file(path_msg)

        for _ in range(20):
            methods.medical_challenge_7(
                do_anomaly=True, msg=msg, is_test=True
            ) 
            logs_list = logs.history.copy() 
            logs.history = []
            meas_mode, ver_mode = False, False
            for log in logs_list:
                if "measurement" in log.lower():
                    meas_mode = True
                if "verification" in log.lower():
                    ver_mode = True

            self.assertTrue(ver_mode and meas_mode)
        
    def test_challenge_8_nominal(self) -> None: 
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()
        msg = methods.Messages.from_file(path_msg)

        for _ in range(20):
            methods.medical_challenge_8(
                do_anomaly=False, msg=msg, is_test=True
            ) 
            logs_list = logs.history.copy() 
            logs.history = []
            meas_mode, ver_mode = False, False
            for log in logs_list:
                if "measurement" in log.lower():
                    meas_mode = True
                if "verification" in log.lower():
                    ver_mode = True

            self.assertTrue(ver_mode and meas_mode)

    def test_challenge_8_anominal(self) -> None: 
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()
        msg = methods.Messages.from_file(path_msg)

        for _ in range(20):
            methods.medical_challenge_8(
                do_anomaly=True, msg=msg, is_test=True
            ) 
            logs_list = logs.history.copy() 
            logs.history = []
            meas_mode, ver_mode = False, False
            for log in logs_list:
                if "measurement" in log.lower():
                    meas_mode = True
                if "verification" in log.lower():
                    ver_mode = True

            self.assertTrue(meas_mode)
            self.assertFalse(ver_mode)