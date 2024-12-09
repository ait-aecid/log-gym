
import unittest
import os


class LogsTestCase(unittest.TestCase):
    def test_change_logs(self) -> None:
        import backbone.logs as logs
        self.assertTrue(logs.store_logs)

        logs.store_logs = False
        logs.path_logs = "test/logs_tests/"
        self.assertFalse(logs.store_logs)
        self.assertEqual(logs.path_logs, "test/logs_tests/")

    def test_store_logs(self) -> None:
        import backbone.logs as logs
        logs.as_test()
        logs.store_logs = True
        logs.path_logs = "test/logs_tests/store_logs.log"
        logs.history = []
        if os.path.isfile(logs.path_logs):
            os.remove(logs.path_logs)
        logs.update_configuration()        
        logs.info("hello")

        self.assertListEqual([" INFO:Test hello"], logs.history)
        self.assertTrue(os.path.isfile(logs.path_logs))

    def test_swap_store_logs(self) -> None:
        path_1 = "test/logs_tests/store_logs.log"
        path_2 = "test/logs_tests/store_logs2.log"

        for path in [path_1, path_2]:
            if os.path.isfile(path_1):
                os.remove(path)

        import backbone.logs as logs
        logs.as_test()
        logs.store_logs = True
        logs.path_logs = path_1
        logs.update_configuration()        
        logs.info("hello")
        logs.info("Cioo")
        self.assertTrue(os.path.isfile(path_1))

        logs.path_logs = path_2
        logs.update_configuration()        
        logs.info("dark rise")
        self.assertTrue(os.path.isfile(path_2))

    def test_not_store_logs(self) -> None:
        import backbone.logs as logs
        logs.as_test()
        logs.store_logs = False
        logs.history = []
        logs.path_logs = "test/logs_tests/store_logs.log"
        if os.path.isfile(logs.path_logs):
            os.remove(logs.path_logs)
        logs.update_configuration()        
        logs.info("hello")

        self.assertListEqual([" INFO:Test hello"], logs.history)
        self.assertFalse(os.path.isfile(logs.path_logs))

    def test_messages(self) -> None:
        import backbone.logs as logs
        logs.as_test()
        logs.store_logs = False
        logs.history = []
        logs.info("hello")
        logs.debug("ciao")
        logs.warning("bye")
        logs.error("lets dance")
        logs.trace("hej")

        self.assertListEqual([
            " INFO:Test hello", 
            " DEBUG:Test ciao", 
            " WARNING:Test bye", 
            " ERROR:Test lets dance",
            " TRACE:Test hej"
        ], logs.history)

    def test_messages_none(self) -> None:
        import backbone.logs as logs
        logs.as_test()
        logs.store_logs = False
        logs.history = []
        logs.info(None)
        logs.debug(None)
        logs.warning(None)
        logs.error(None)
        logs.trace(None)

        self.assertListEqual([], logs.history)