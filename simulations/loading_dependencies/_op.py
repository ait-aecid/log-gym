
import numpy as np
import typing as t
import time


class NormDist:
    def __init__(self, radius: float, mu: float, std: float) -> None:
        self.radius = radius
        self.mu = mu
        self.std_2 = std ** 2
        self._c = 1 / np.sqrt(2 * np.pi * self.std_2)

    def __contains__(self, x: float) -> bool:
        return self.min_value() <= x <= self.max_value()

    def min_value(self) -> float:
        return self.mu - self.radius

    def max_value(self) -> float:
        return self.mu + self.radius

    def p(self, x) -> float:
        if x in self:
            return self._c * np.exp(- ((x - self.mu) ** 2) / (2 * self.std_2))
        return np.zeros(len(x)) if isinstance(x, np.ndarray) else 0.   

    def sample(self) -> float:
        candidates = np.linspace(self.min_value(), self.max_value(), num=1000) 
        p = np.array([self.p(c) for c in candidates])
        p /= np.sum(p)
        return float(np.random.choice(candidates, p=p, size=1))


class Dependency:
    def __init__(
        self, nominal: t.Dict[str, float], anominal: t.Dict[str, float]
    ) -> None:
        self.nominalDist = NormDist(
            radius=nominal["radius"], mu=nominal["mu"], std=nominal["std"]
        )
        self.anominalDist = NormDist(
            radius=anominal["radius"], mu=anominal["mu"], std=anominal["std"]
        )
        self.anominal = False
        self.test_reduction = 1.  # speed up tests

    def __call__(self) -> None:
        t = self.anominalDist.sample() if self.anominal else self.nominalDist.sample()
        time.sleep(t / self.test_reduction)


class ConfigDependencies:
    do_anomaly = False
    args_a = {
        "nominal": {"radius": 0.2, "mu": 0.3, "std": 0.5},
        "anominal": {"radius": 0.1, "mu": 3.1, "std": 1.4}
    }
    args_b = {
        "nominal": {"radius": 0.2, "mu": 0.3, "std": 0.5},
        "anominal": {"radius": 0.1, "mu": 3.1, "std": 1.4}
    }
    args_c = {
        "nominal": {"radius": 0.2, "mu": 0.3, "std": 0.5},
        "anominal": {"radius": 0.1, "mu": 3.1, "std": 1.4}
    }
    args_d = {
        "nominal": {"radius": 0.2, "mu": 0.3, "std": 0.5},
        "anominal": {"radius": 0.1, "mu": 3.1, "std": 1.4}
    }


class Dependencies:
    def __init__(
        self,
        config: ConfigDependencies,
        anominal_dependency: t.List[bool] = [False, False, False, False]
    ) -> None:
        self.do_anomaly = config.do_anomaly
        self.__init_dependencies(config=config)        
        self.__config_anomalies(anominal_dependency)

    def __init_dependencies(self, config: ConfigDependencies) -> None:
        depends = ["depend_a", "depend_b", "depend_c", "depend_d"]
        args_ = [config.args_a, config.args_b, config.args_c, config.args_d]
        self.dep = []
        for depend, args in zip(depends, args_):
            self.dep.append(Dependency(
                nominal=args["nominal"], anominal=args["anominal"]
            ))
            setattr(self, depend, self.dep[-1])

    def __config_anomalies(self, anominal_dependency: t.List[bool]) -> None:
        for depend, is_anominal in zip(self.dep, anominal_dependency):
            depend.anominal = self.do_anomaly and is_anominal

    def add_test_reduction(self, reduction: float) -> None:
        for depend in self.dep:
            depend.test_reduction = reduction

    def load_a(self) -> None:
        self.depend_a()

    def load_b(self) -> None:
        self.depend_b()

    def load_c(self) -> None:
        self.depend_c()

    def load_d(self) -> None:
        self.depend_d()
