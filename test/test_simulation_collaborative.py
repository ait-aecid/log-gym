from simulations.collaborative_setup import methods

import unittest


path_msg = "simulations/collaborative_setup/messages.yaml"

class SenderTestCase(unittest.TestCase):
    def setUp(self):
        self.msg = methods.Messages.from_file(path_msg, version=1)

    def test_sender_template_1(self):
        import backbone.logs as logs
        logs.store_logs = False
        logs.as_test()
        logs.history = []

        sender = methods.Sender(do_anomaly=False, msg=self.msg, client_n=0)
        sender.send_package()

        self.assertListEqual(
            [" INFO:Test <*template_1*>Sending file with package 1"], logs.history
        )

    def test_sender_template_2(self):
        import backbone.logs as logs
        logs.store_logs = False
        logs.as_test()
        logs.history = []

        sender = methods.Sender(do_anomaly=False, msg=self.msg, client_n=1)
        sender.send_package()
        sender = methods.Sender(do_anomaly=False, msg=self.msg, client_n=2)
        sender.send_package()

        self.assertListEqual(
            [
                " INFO:Test <*template_2*>Sending file with package 1",
                " INFO:Test <*template_2*>Sending file with package 1",
            ], logs.history
        )

    def test_sender_template_1_error(self):
        import backbone.logs as logs
        logs.store_logs = False
        logs.as_test()
        logs.history = []

        sender = methods.Sender(do_anomaly=True, msg=self.msg, client_n=0)
        sender.send_package()

        self.assertListEqual(
            [" INFO:Test <*template_1*>Sending file with package 1 Failed"], logs.history
        )

    def test_sender_template_2_error(self):
        import backbone.logs as logs
        logs.store_logs = False
        logs.as_test()
        logs.history = []

        sender = methods.Sender(do_anomaly=True, msg=self.msg, client_n=1)
        sender.send_package()
        sender = methods.Sender(do_anomaly=True, msg=self.msg, client_n=2)
        sender.send_package()

        self.assertListEqual(
            [
                " INFO:Test <*template_2*>Sending file with package 1 Failed",
                " INFO:Test <*template_2*>Sending file with package 1 Failed",
            ], logs.history
        )

    def test_sender_wait(self):
        import backbone.logs as logs
        logs.store_logs = False
        logs.as_test()
        logs.history = []

        sender = methods.Sender(do_anomaly=False, msg=self.msg, client_n=0, is_test=True)
        gen = sender.wait_to_send()
        while next(gen): pass
        self.assertListEqual(
            [" INFO:Test Waiting..." for _ in range(4)], logs.history
        )

        logs.history = []
        sender = methods.Sender(do_anomaly=True, msg=self.msg, client_n=0, is_test=True)
        gen = sender.wait_to_send()
        while next(gen): pass
        self.assertListEqual(
            [" INFO:Test Waiting..." for _ in range(10)], logs.history
        )

class AdminAcessTestCase(unittest.TestCase):
    def test_is_anomaly(self):
        for i in range(10):
            self.assertTrue(methods.is_admin(do_anomaly=True, client_n=i))

    def test_is_nominal(self):
        for i in range(10):
            if i == 0:
                self.assertTrue(methods.is_admin(do_anomaly=False, client_n=i))
            else:
                self.assertFalse(methods.is_admin(do_anomaly=False, client_n=i))