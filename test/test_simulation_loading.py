from simulations.loading_dependencies import methods
from simulations.loading_dependencies import _op

from typing import List
import time

import unittest


class DistTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.norm = _op.NormDist(radius=0.4, mu=2, std=0.5)

    def test_dist_min_max(self) -> None:
        self.assertAlmostEqual(self.norm.max_value(), 2.4, delta=1e-4)
        self.assertAlmostEqual(self.norm.min_value(), 1.6, delta=1e-4)

    def test_probability_density_out(self) -> None:
        self.assertAlmostEqual(self.norm.p(2.8), 0., delta=1e-4)
        self.assertAlmostEqual(self.norm.p(0.8), 0., delta=1e-4)

    def test_probability_density(self) -> None:
        self.assertAlmostEqual(self.norm.p(2), 0.79788, delta=1e-4)
        self.assertAlmostEqual(self.norm.p(2.22), 0.72427, delta=1e-4)
        self.assertAlmostEqual(self.norm.p(1.8), 0.7365, delta=1e-4)

    def test_sample(self) -> None:
        old_value = 0
        i = 0
        for _ in range(100):
            self.assertTrue(1.6 <= (value := self.norm.sample()) <= 2.4)
            i = i + 1 if old_value == value else i
            if i > 5:
                self.assertNotEqual(old_value, value)
            old_value = value


class DependenciesTestCase(unittest.TestCase):
    def test_dependency(self) -> None:
        dependency = _op.Dependency(
            nominal={"radius": 0.2, "mu": 0.3, "std": 0.5},
            anominal={"radius": 0.1, "mu": 3.1, "std": 1.4}
        )
        dependency.test_reduction = (m := 250)
        
        for _ in range(4):
            start = time.time()
            dependency()
            end = time.time() - start
            self.assertTrue(end < (1.5 / m))

    def test_dependency_anominal(self) -> None:
        dependency = _op.Dependency(
            nominal={"radius": 0.2, "mu": 0.3, "std": 0.5},
            anominal={"radius": 0.1, "mu": 3.1, "std": 1.4}
        )
        dependency.test_reduction = (m := 250)
        dependency.anominal = True
        
        for _ in range(4):
            start = time.time()
            dependency()
            end = time.time() - start
            self.assertTrue(end > (1.5 / m))

    def check(self, name_dep: str, anominal_dependency: List[bool]) -> None:
        m = 250

        dependencies = _op.Dependencies(config=_op.ConfigDependencies())
        dependencies.add_test_reduction(m)
        for _ in range(4):
            start = time.time()
            getattr(dependencies, name_dep)()
            end = time.time() - start
            self.assertTrue(end < (1.5 / m))

        config = _op.ConfigDependencies()
        config.do_anomaly = True
        dependencies = _op.Dependencies(
            config=config, anominal_dependency=anominal_dependency
        )
        dependencies.add_test_reduction(m)
        for _ in range(4):
            start = time.time()
            getattr(dependencies, name_dep)()
            end = time.time() - start
            self.assertTrue(end > (1.5 / m))

    def test_dependency_a(self) -> None:
        self.check("load_a", [True, False, False, False])

    def test_dependency_b(self) -> None:
        self.check("load_b", [False, True, False, False])

    def test_dependency_c(self) -> None:
        self.check("load_c", [False, False, True, False])

    def test_dependency_d(self) -> None:
        self.check("load_d", [False, False, False, True])

    def test_no_anominal(self) -> None:
        m = 250
        dependencies = _op.Dependencies(
            config=_op.ConfigDependencies(), 
            anominal_dependency=[True, True, True, True]
        )
        dependencies.add_test_reduction(m)
        for _ in range(4):
            start = time.time()
            getattr(dependencies, "load_a")()
            end = time.time() - start
            self.assertTrue(end < (1.5 / m))


path_msg = "simulations/loading_dependencies/messages.yaml"

class CasesTestCase(unittest.TestCase):
    def test_challenge_4_dont_break(self) -> None:
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        msg = methods.Messages.from_file(path_msg)
        methods.dependencies_challenge_4(do_anomaly=False, msg=msg, reduction=700)

        msg = methods.Messages.from_file(path_msg)
        methods.dependencies_challenge_4(do_anomaly=True, msg=msg, reduction=700)

    def test_challenge_5_dont_break(self) -> None:
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        msg = methods.Messages.from_file(path_msg)
        methods.dependencies_challenge_5(do_anomaly=False, msg=msg, reduction=700)

        msg = methods.Messages.from_file(path_msg)
        methods.dependencies_challenge_5(do_anomaly=True, msg=msg, reduction=700)

    def test_challenge_6_dont_break(self) -> None:
        import backbone.logs as logs 
        logs.store_logs = False
        logs.as_test()

        msg = methods.Messages.from_file(path_msg)
        methods.dependencies_challenge_6(do_anomaly=False, msg=msg, reduction=700)

        msg = methods.Messages.from_file(path_msg)
        methods.dependencies_challenge_6(do_anomaly=True, msg=msg, reduction=700)

    def test_condition_method(self) -> None:
        self.assertFalse(all([methods.condition() for _ in range(10)]))
        self.assertTrue(any([methods.condition() for _ in range(10)]))