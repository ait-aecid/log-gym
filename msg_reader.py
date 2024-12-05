
import typing as t
import yaml


class Data:
    def __init__(self, list_msg: t.Dict[str, str]) -> None:
        self.list_msg = list_msg
        for k, v in self.list_msg.items():
            setattr(self, k, v)

    def __getitem__(self, msg_name: str) -> str:
        return self.list_msg[msg_name]


class Messages:
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
                    self.list_msgs[name] = msgs[name][log]
                    setattr(self, name, self.list_msgs[name])
                elif self.__is_template(log):
                    templates[name] = msgs[name][log]

            if name not in self.list_msgs:
                self.list_msgs[name] = None
                setattr(self, name, self.list_msgs[name])
                templates[name] = None

        self.templates = Data(templates)   

    def __init__(self, msgs: t.Dict[str, str], version: int = 1) -> None:
        self.version  = version
        self.__initialize(msgs=msgs)

    @classmethod
    def from_file(cls, path_file: str, version: int = 1) -> object:
        with open(path_file, "r") as f:
            msgs = yaml.safe_load(f)
        return cls(msgs=msgs, version=version)

    def __getitem__(self, msg_name: str) -> str:
        return self.list_msgs[msg_name]

