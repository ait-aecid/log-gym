from simulations.access_resource.methods import (
    Resource, 
    ConfigResource,
    case1_init_resource,    
    case2_init_resource,
    case3_init_resource,
)
from simulations.access_resource.simulation import main
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

    def test_case1_nominal(self):
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        config = ConfigResource()
        config.wait_time = 0
        logs.history = []
        msg = Messages.from_file(path_msg)
        case1_init_resource(config, msg=msg)
        self.assertTrue(" INFO:Test Resource ready" in logs.history)

    def test_case1_anominal(self):
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        config = ConfigResource()
        config.do_anomaly = True
        config.wait_time = 0
        logs.history = []
        msg = Messages.from_file(path_msg)
        case1_init_resource(config, msg=msg)
        self.assertTrue(" INFO:Test Resource ready" not in logs.history)

    def test_case2_nominal(self):
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        config = ConfigResource()
        config.wait_time = 0
        logs.history = []
        msg = Messages.from_file(path_msg)
        case2_init_resource(config, msg=msg)
        self.assertTrue(" INFO:Test Resource ready" in logs.history)

    def test_case2_anominal(self):
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        config = ConfigResource()
        config.do_anomaly = True
        config.wait_time = 0
        logs.history = []
        msg = Messages.from_file(path_msg)
        case2_init_resource(config, msg=msg)
        self.assertTrue(" INFO:Test Resource ready" not in logs.history)

    def test_case3_nominal(self):
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        config = ConfigResource()
        config.wait_time = 0
        logs.history = []
        msg = Messages.from_file(path_msg)
        case3_init_resource(config, msg=msg)
        self.assertTrue(" INFO:Test Errors found False" in logs.history)

    def test_case3_anominal(self):
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        config = ConfigResource()
        config.do_anomaly = True
        config.wait_time = 0
        logs.history = []
        msg = Messages.from_file(path_msg)
        case3_init_resource(config, msg=msg)
        self.assertTrue(" INFO:Test Errors found True" in logs.history)

    def test_main(self):
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        config = ConfigResource()
        config.do_anomaly = True
        config.wait_time = 0
        logs.history = []
        msg = Messages.from_file(path_msg)
        main(case="case_1", config=config, msg=msg)
        self.assertTrue(" TRACE:Test Process has started" in logs.history)
        self.assertTrue(" TRACE:Test Process has ended" in logs.history)