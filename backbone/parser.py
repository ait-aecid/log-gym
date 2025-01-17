from backbone.msg_reader import Messages, Templates

import pandas as pd
import typing as t
import re


class ParserMethods:
    @staticmethod
    def __it_has_clients(logs: t.List[str]) -> bool:
        for log in logs:
            if "<*Client_" in log:
                return True

    @staticmethod
    def structure_logs(logs: t.List[str]) -> t.Dict[str, t.List[str]]:
        structured = {k: [] for k in [
            "Level", "Module", "Date", "Time", "Content"
        ]}
        if (has_clients := ParserMethods.__it_has_clients(logs)):
            client_pattern = re.compile(r"<\*Client_(\d+)\*>")
            message_pattern = re.compile(r"<\*Client_\d+\*>(.*)")
            structured["Client"] = []

        for log in logs:
            log_ = ":".join(log.split(":")[2:])
            date_time = log_.replace("[", "").split("]")[0]
            rest = log_[1:].replace(date_time, "").replace("] ", "")
            level_module = rest.split(" ")[0]

            structured["Level"].append(level_module.split(":")[0])
            structured["Module"].append(level_module.split(":")[1])
            structured["Date"].append(date_time.split("/")[0])
            structured["Time"].append(date_time.split("/")[1])

            rest = rest.replace(level_module, "")[1:]
            if has_clients:
                client = client_pattern.search(rest).group(1)
                structured["Client"].append(int(client))
                rest = message_pattern.search(rest).group(1) 
            structured["Content"].append(rest)

        return structured


    @staticmethod
    def get_variables(
        structured_logs: t.Dict[str, t.List[str]]
    ) -> t.Dict[str, t.List[str]]:
        
        structured_logs["Variables"] = []
        for log, temp in zip(
            structured_logs["Content"], structured_logs["Template"]
        ):
            temp_words = temp.split("<*>") 
            log_words = log.split(" ")
            structured_logs["Variables"].append([
                word for word in log_words 
                if not any([word in tword for tword in temp_words])
            ])

        return structured_logs

    @staticmethod
    def get_events(
        structured_logs: t.Dict[str, t.List[str]], 
        list_msgs: t.Dict[str, t.List[str]],
        templates: Templates,
    ) -> t.Dict[str, t.List[str]]:
        
        temp_df = templates.as_dataframe()
        templates_logs, event_ids = [], []
        for log in structured_logs["Content"]:
            found_it = False
            for name, msg in list_msgs.items():
                if log == msg:
                    templates_logs.append(templates[name])
                    idx = temp_df["Template"] == templates_logs[-1]
                    event_ids.append(temp_df["Event ID"][idx].iloc[0])
                    found_it = True
                    break
            assert found_it, f"({log}) was not found"

        structured_logs["Template"] = templates_logs
        structured_logs["Event ID"] = event_ids

        return structured_logs


class Parser(Messages):
    """
    Class use for the parsing of the logs
    """
    def __init__(
        self, msgs: t.Dict[str, str], version: int = 1, client_n: None = None
    ) -> None:
        super().__init__(msgs, version, client_n=client_n)

    @classmethod
    def from_file(cls, path_file: str, version: int = 1) -> t.Self:
        return super().from_file(path_file, version, client_n=None)
 
    def __add_structured_logs(self, logs: t.List[str]) -> pd.DataFrame:

        structured_logs = ParserMethods.structure_logs(logs)
        structured_logs = ParserMethods.get_events(
            structured_logs=structured_logs, 
            list_msgs=self.list_msgs, 
            templates=self.templates
        ) 
        structured_logs = ParserMethods.get_variables(structured_logs)
        return pd.DataFrame(structured_logs)

    def __call__(self, logs: t.List[str]) -> t.Dict[str, pd.DataFrame]:
        results = {"Templates": self.templates.as_dataframe()} 
        results["Structured logs"] = self.__add_structured_logs(logs=logs)
        return results

    def load_logs(self, path_logs: str) -> t.Dict[str, pd.DataFrame]:
        with open(path_logs, "r") as f:
            return self([log.replace("\n", "") for log in f.readlines()])