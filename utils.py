import typing as t
import yaml


class Color:
    @staticmethod
    def purple(msg: str) -> str:
        return f"\033[95m{msg}\033[0m"

    @staticmethod
    def blue(msg: str) -> str:
        return f"\033[94m{msg}\033[0m"

    @staticmethod
    def green(msg: str) -> str:
        return f"\033[92m{msg}\033[0m"

    @staticmethod
    def yellow(msg: str) -> str:
        return f"\033[93m{msg}\033[0m"

    @staticmethod
    def red(msg: str) -> str:
        return f"\033[91m{msg}\033[0m"


def read_yaml_file(path: str): 
    with open(path) as file:
        return yaml.safe_load(file)


class Config:
    def __init__(
        self,
        path: str, 
        read_file: t.Callable[[str], t.Dict[str, t.Any]] = read_yaml_file
    ) -> None:
        self.__config = read_file(path)

    def get_parameters(self) -> t.Tuple[str, str, str]:
        return (
            self.__config["General"]["Simulation"],
            self.__config["General"]["Case"],
            self.__config["General"]["Save_path"]
        )
    
    def simulations(self) -> t.List[str]:
        return [k for k in self.__config.keys() if k != "General"]
    
    def __getitem__(self, idx: str) -> t.Dict[str, t.Any]:
        return self.__config[idx] 