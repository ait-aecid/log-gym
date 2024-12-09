import pandas as pd
import typing as t


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

    def save(path: str) -> None:
        pass


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

    def save(path: str) -> None:
        pass


def split_in_process(structured_logs: pd.DataFrame) -> t.Iterable[pd.DataFrame]:
    idx = [i for i, info in enumerate(structured_logs["Level"]) if info == "TRACE"]
    idx = [(idx[i], idx[i+1]) for i in range(0, len(idx), 2)]
    for i, j in idx:
        yield structured_logs.iloc[i + 1:j]


def process_table(
    structured_logs: pd.DataFrame, tempSet: TemplateSet
) -> Dataset:
    dataset = Dataset()
    for table in split_in_process(structured_logs):
        dataset["Level"] = table["Level"].to_list()

    return dataset