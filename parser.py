from msg_reader import Messages, Data

import pandas as pd
import typing as t


class ParserMethods:
    @staticmethod
    def structure_logs(logs: t.List[str]) -> t.Dict[str, t.List[str]]:
        structured = {k: [] for k in [
            "Level", "Module", "Date", "Time", "Content"
        ]}
        for log in logs:
            log_ = ":".join(log.split(":")[2:])
            date_time = log_.replace("[", "").split("]")[0]
            rest = log_[1:].replace(date_time, "").replace("] ", "")
            level_module = rest.split(" ")[0]

            structured["Level"].append(level_module.split(":")[0])
            structured["Module"].append(level_module.split(":")[1])
            structured["Date"].append(date_time.split("/")[0])
            structured["Time"].append(date_time.split("/")[1])
            structured["Content"].append(rest.replace(level_module, "")[1:])

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


def get_events(
    structured_logs: t.Dict[str, t.List[str]], 
    templates: pd.DataFrame,
    list_msgs: t.Dict[str, t.List[str]],
    templates_inst: Data,
) -> t.Dict[str, t.List[str]]:
    
    templates_logs, event_ids = [], []
    for log in structured_logs["Content"]:
        found_it = False
        for name, msg in list_msgs.items():
            if log == msg:
                templates_logs.append(templates_inst[name])
                idx = templates["Template"] == templates_logs[-1]
                event_ids.append(templates["Event ID"][idx].iloc[0])
                found_it = True
                break
        assert found_it, f"({log}) was not found"

    structured_logs["Template"] = templates_logs
    structured_logs["Event ID"] = event_ids

    return structured_logs


class Parser(Messages):
    def __init__(self, msgs: t.Dict[str, str], version: int = 1) -> None:
        super().__init__(msgs, version)

    @classmethod
    def from_file(cls, path_file: str, version: int = 1) -> t.Self:
        return super().from_file(path_file, version)

    def __add_templates(self) -> pd.DataFrame:
        df = pd.DataFrame(
            {"Template": list(set(self.templates.list_msg.values()))}
        )
        df["Event ID"] = list(df.index)
        return df
    
    def __add_structured_logs(
        self, logs: t.List[str], templates: pd.DataFrame
    ) -> pd.DataFrame:
        structured_logs = ParserMethods.structure_logs(logs)
        structured_logs = get_events(
            structured_logs=structured_logs, 
            templates=templates, 
            list_msgs=self.list_msgs, 
            templates_inst=self.templates
        ) 
        structured_logs = ParserMethods.get_variables(structured_logs)
        return pd.DataFrame(structured_logs)

    def __call__(self, logs: t.List[str]) -> t.Dict[str, pd.DataFrame]:
        results = {"Templates": self.__add_templates()}
        results["Structured logs"] = self.__add_structured_logs(
            logs=logs, templates=results["Templates"]
        )
        return results

    def load_logs(self, path_logs: str) -> t.Dict[str, pd.DataFrame]:
        with open(path_logs, "r") as f:
            return self([log.replace("\n", "") for log in f.readlines()])