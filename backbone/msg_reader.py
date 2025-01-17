from utils import read_yaml_file

import pandas as pd
import typing as t


class Templates:
    """
    Wrapper class for the different log templates
    """
    def __init__(self, list_msg: t.Dict[str, str]) -> None:
        self.list_msg = list_msg
        for k, v in self.list_msg.items():
            setattr(self, k, v)

    def as_dataframe(self):
        df = pd.DataFrame(
            {"Template": list(set(self.list_msg.values()))}
        )
        df["Event ID"] = list(df.index)
        return df

    def __getitem__(self, msg_name: str) -> str:
        return self.list_msg[msg_name]


class Messages:
    """
    Manager class of all the log and template messages.    
    """
    def __is_log(self, msg: str) -> bool:
        return msg.startswith(f"v{self.version}") and "template" not in msg

    def __is_template(self, msg: str) -> bool:
        return msg.startswith(f"v{self.version}") and "template" in msg

    def __initialize(self, msgs: t.Dict[str, str]) -> None:
        self.list_msgs = {}
        templates = {}
        for name, logs in msgs.items():
            for log in logs:
                if self.__is_log(log):
                    self.list_msgs[name] = f"{self.prefix}{msgs[name][log]}"
                    setattr(self, name, self.list_msgs[name])
                elif self.__is_template(log):
                    templates[name] = msgs[name][log]

            if name not in self.list_msgs:
                self.list_msgs[name] = None
                setattr(self, name, self.list_msgs[name])
                templates[name] = None

        self.templates = Templates(templates)   

    def __init__(
        self, msgs: t.Dict[str, str], version: int = 1, client_n: int | None = None
    ) -> None:
        self.version  = version
        self.prefix = "" if client_n is None else f"<*Client_{client_n}*>"
        self.__initialize(msgs=msgs)

    @classmethod
    def from_file(
        cls, path_file: str, version: int = 1, client_n: int | None = None
    ) -> object:
        msgs = read_yaml_file(path_file)
        return cls(msgs=msgs, version=version, client_n=client_n)

    def __getitem__(self, msg_name: str) -> str:
        return self.list_msgs[msg_name]

