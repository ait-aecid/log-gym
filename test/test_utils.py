
import utils

import unittest


def read_config(path):
    return {
        "General": {
            "Simulation": "simulation",
            "Case": "case_2",
            "Save_path": "Hello",
        },
        "Train": {"hello": "world"},
        "Test_1": {"ciao": "bella"},
        "Test_2": {"wie": "geht's"},
    }


class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.config = utils.Config("", read_file=read_config)

    def test_get_params(self) -> None:
        self.assertTupleEqual(
            self.config.get_parameters(), ("simulation", "case_2", "Hello")
        )

    def test_simulations(self) -> None:
        simulations = self.config.simulations()

        self.assertEqual(3, len(simulations))
        self.assertSetEqual(
            set(simulations), {"Train", "Test_1", "Test_2"}
        )

    def test_get_params_simulations(self) -> None:
        self.assertDictEqual(self.config["Train"], {"hello": "world"})
        self.assertDictEqual(self.config["Test_1"], {"ciao": "bella"})
        self.assertDictEqual(self.config["Test_2"], {"wie": "geht's"})