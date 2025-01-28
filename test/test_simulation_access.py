from simulations.access_resource.methods import (
    Resource, 
    ConfigResource,
    resources_challenge_1,    
    resources_challenge_2,
    resources_challenge_3,
)
from simulations.access_resource.simulation import AccessResources
from backbone.msg_reader import Messages

import unittest


path_msg = "simulations/access_resource/messages.yaml"

class ProcessTestCase(unittest.TestCase):
    def test_do_anomaly(self):        
        for _ in range(10):
            config = ConfigResource()
            resource = Resource(config=config)
            value_1 = 0
            for _ in range(100):
                value_1 += int(resource.init())

            config.do_anomaly = True
            resource = Resource(config=config)
            value_2 = 0
            for _ in range(100):
                value_2 += int(resource.init())

            self.assertTrue(value_1 > value_2)

    def test_nominals_maller_max_iter(self):
        config = ConfigResource()
        config.max_iter = 10
        config.p_normal = [1., 0.]
        
        resource = Resource(config=config)
        for i in range(config.max_iter + 2):
            if resource.init(i):
                break
        self.assertEqual(config.max_iter, i)   

    def test_challenge_1_nominal(self):
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        config = ConfigResource()
        config.wait_time = 0
        logs.history = []
        msg = Messages.from_file(path_msg)
        resources_challenge_1(config, msg=msg)
        self.assertTrue(" INFO:Test Resource ready" in logs.history)

    def test_challenge_1_anominal(self):
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        config = ConfigResource()
        config.do_anomaly = True
        config.wait_time = 0
        logs.history = []
        msg = Messages.from_file(path_msg)
        resources_challenge_1(config, msg=msg)
        self.assertTrue(" INFO:Test Resource ready" not in logs.history)

    def test_challenge_2_nominal(self):
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        config = ConfigResource()
        config.wait_time = 0
        logs.history = []
        msg = Messages.from_file(path_msg)
        resources_challenge_2(config, msg=msg)
        self.assertTrue(" INFO:Test Resource ready" in logs.history)

    def test_challenge_2_anominal(self):
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        config = ConfigResource()
        config.do_anomaly = True
        config.wait_time = 0
        logs.history = []
        msg = Messages.from_file(path_msg)
        resources_challenge_2(config, msg=msg)
        self.assertTrue(" INFO:Test Resource ready" not in logs.history)

    def test_challenge_3_nominal(self):
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        config = ConfigResource()
        config.wait_time = 0
        logs.history = []
        msg = Messages.from_file(path_msg)
        resources_challenge_3(config, msg=msg)
        self.assertTrue(" INFO:Test Errors found None" in logs.history)

    def test_challenge_3_anominal(self):
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        config = ConfigResource()
        config.do_anomaly = True
        config.wait_time = 0
        logs.history = []
        msg = Messages.from_file(path_msg)
        resources_challenge_3(config, msg=msg)
        self.assertTrue(" INFO:Test Errors found None" not in logs.history)
