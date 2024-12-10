from datetime import datetime

import pandas as pd
import typing as t

# %% Data structures
class TemplateSet:
    def __init__(self) -> None:
        self._temp = {}

    def __len__(self) -> int:
        return len(self._temp)

    def __contains__(self, value) -> bool:
        return value in self._temp.keys()

    def add(self, templates: pd.DataFrame) -> None:
        for template in templates["Template"].to_list():
            if template not in self and template != "":
                self._temp[template] = len(self)

    def __getitem__(self, idx: str) -> int:
        return self._temp[idx]

    def save(self, path: str) -> None:
        pd.DataFrame({
            "Template": self._temp.keys(), "Event ID": self._temp.values()
        }).to_csv(path, index=False)


class Dataset:
    def __init__(self) -> None:
        self._dataset = {}
 
    def __contains__(self, value) -> bool:
        return value in self._dataset.keys()

    def __setitem__(self, idx: str, value: t.Any) -> None:
        if idx not in self:
            self._dataset[idx] = []
        self._dataset[idx].append(value)

    def __getitem__(self, idx: str) -> t.List[t.Any]:
        return self._dataset[idx]

    def save(self, path: str) -> None:
        pd.DataFrame(self._dataset).to_csv(path, index=False)


# %% Auxiliar methods
def split_in_process(structured_logs: pd.DataFrame) -> t.Iterable[pd.DataFrame]:
    idx = [i for i, info in enumerate(structured_logs["Level"]) if info == "TRACE"]
    idx = [(idx[i], idx[i+1]) for i in range(0, len(idx), 2)]
    for i, j in idx:
        yield structured_logs.iloc[i + 1:j]


def get_time_diff(dates: t.List[str], times: t.List[str]) -> t.List[int]:
    format = "%Y-%m-%d//%H:%M:%S"
    time_stamps = [
        datetime.strptime(f"{date}//{time}", format).timestamp() 
        for date, time in zip(dates, times)
    ]

    return [
        int(time_stamps[i] - time_stamps[i - 1]) 
        for i in range(1, len(time_stamps))
    ]


def process_table(
    structured_logs: pd.DataFrame, tempSet: TemplateSet
) -> Dataset:

    dataset = Dataset()
    for table in split_in_process(structured_logs):
        dataset["Level"] = table["Level"].to_list()
        dataset["Content"] = table["Content"].to_list()
        dataset["Template"] = table["Template"].to_list()
        dataset["Event ID"] = [
            tempSet[temp] for temp in table["Template"].tolist() 
        ]
        dataset["Time Diff"] = get_time_diff(
            dates=table["Date"].to_list(), times=table["Time"].to_list()
        )

    return dataset


# %% Main method
def process_all_tables(
    structured_logs_paths: t.List[str], template_paths: t.List[str], save_path: str,
) -> None:
    """
    Process all the tables so they can be use in training
    """
    tempSet = TemplateSet()
    for template_path in template_paths:
        tempSet.add(pd.read_csv(template_path))
    tempSet.save(f"{save_path}/template.csv")
    
    for structured_logs_path in structured_logs_paths:
        name = structured_logs_path.split("/")[-2]
        process_table(
            pd.read_csv(structured_logs_path), tempSet=tempSet
        ).save(f"{save_path}/{name}.csv")