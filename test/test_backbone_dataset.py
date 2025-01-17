import backbone.dataset_generator as dg

import pandas as pd
import unittest 


class TemplateSetTestCase(unittest.TestCase):
    def test_add_templates(self) -> None:
        tempSet = dg.TemplateSet()
        tempSet.add(
            pd.DataFrame({"Template": ["", "AB"], "Event ID": [0, 1]})
        )
        tempSet.add(
            pd.DataFrame({"Template": ["CD", "AB"], "Event ID": [0, 1]})
        )

        self.assertDictEqual(tempSet._temp, {"AB": 0, "CD": 1})

    def test_get_event_id(self) -> None:
        tempSet = dg.TemplateSet()
        tempSet.add(
            pd.DataFrame({"Template": ["CD", "AB"], "Event ID": [0, 1]})
        )

        self.assertEqual(tempSet["CD"], 0) 
        self.assertEqual(tempSet["AB"], 1) 


class DatasetTestCase(unittest.TestCase):
    def test_set_empty_item(self) -> None:
        dataset = dg.Dataset()
        dataset["hi"] = [4, 3]

        self.assertListEqual(dataset["hi"], [[4, 3]])

    def test_set_item(self) -> None:
        dataset = dg.Dataset()
        dataset["hi"] = [4, 3]
        dataset["hi"] = [1, 2]

        self.assertListEqual(dataset["hi"], [[4, 3], [1, 2]])


first_expected = {
    "Level": ["INFO", "INFO"],
    "Module": ["Standard", "Standard"],
    "Date": ["2024-12-09", "2024-12-09"],
    "Time": ["13:28:26", "13:28:27"],
    "Content": ["Trying again later", "Resource ready"],
    "Template": ["Trying again later", "Resource ready"],
    "Event ID": [4, 3],
    "Variables":["[]", "[]"]
}


second_expected = {
    "Level": ["INFO"],
    "Module": ["Standard"],
    "Date": ["2024-12-09"],
    "Time": ["13:28:27"],
    "Content": ["Resource ready"],
    "Template": ["Resource ready"],
    "Event ID": [3],
    "Variables":["[]"]
}


third_expected = {
    "Level": ["INFO", "INFO"],
    "Module": ["Standard", "Standard"],
    "Date": ["2024-12-09", "2024-12-09"],
    "Time": ["13:28:27", "13:28:28"],
    "Content": ["Trying again later", "Resource ready"],
    "Template": ["Trying again later", "Resource ready"],
    "Event ID": [4, 3],
    "Variables":["[]", "[]"]
}


path_logs = "test/logs_tests/structured_logs.csv"
path_logs_clients = "test/logs_tests/structured_logs_clients.csv"

 
class DataGeneratorTestCase(unittest.TestCase):
    def test_split_process(self) -> None:
        gen = dg.split_in_process(pd.read_csv(path_logs))
        expected = [first_expected, second_expected, third_expected]
        for z, table in enumerate(gen):
            table_ = table.to_dict("list")
            for k in table_.keys():
                self.assertListEqual(expected[z][k], table_[k])
        self.assertEqual(2, z)

    def test_split_process_n_clients(self) -> None:
        gen = dg.split_in_process(pd.read_csv(path_logs_clients))
        expected = [first_expected, second_expected, third_expected]
        first_expected["Client"] = [0, 0]
        second_expected["Client"] = [1]
        third_expected["Client"] = [2, 2]

        for z, table in enumerate(gen):
            table_ = table.to_dict("list")
            for k in table_.keys():
                self.assertListEqual(expected[z][k], table_[k])
        self.assertEqual(2, z)

    def test_time_diff(self) -> None:
        date = ["2024-12-09", "2024-12-09", "2024-12-10"]
        time = ["13:28:27", "13:28:29", "13:28:29"]
        result = dg.get_time_diff(dates=date, times=time)

        self.assertListEqual([2, 86400], result)

    def test_process_table(self) -> None:
        tempSet = dg.TemplateSet()
        tempSet.add(
            pd.DataFrame({
                "Template": ["Trying again later", "Resource ready"], 
                "Event ID": [0, 1]
            })
        )
        dataset = dg.process_table(pd.read_csv(path_logs), tempSet=tempSet)

        self.assertTrue("Client" not in dataset)
        self.assertListEqual(
            [["INFO", "INFO"], ["INFO"], ["INFO", "INFO"]], dataset["Level"]
        )
        self.assertListEqual(
            [
                ["Trying again later", "Resource ready"],
                ["Resource ready"], 
                ["Trying again later", "Resource ready"]
            ], dataset["Content"]
        )
        self.assertListEqual(
            [
                ["Trying again later", "Resource ready"],
                ["Resource ready"], 
                ["Trying again later", "Resource ready"]
            ], dataset["Template"]
        )
        self.assertListEqual([[0, 1], [1], [0, 1]], dataset["Event ID"])
        self.assertListEqual([[1.], [], [1.]], dataset["Time Diff"])

    def test_process_table_clients(self) -> None:
        tempSet = dg.TemplateSet()
        tempSet.add(
            pd.DataFrame({
                "Template": ["Trying again later", "Resource ready"], 
                "Event ID": [0, 1]
            })
        )
        dataset = dg.process_table(pd.read_csv(path_logs_clients), tempSet=tempSet)

        self.assertListEqual(
            [["INFO", "INFO"], ["INFO"], ["INFO", "INFO"]], dataset["Level"]
        )
        self.assertListEqual([[0, 0], [1], [2, 2]], dataset["Client"])
        self.assertListEqual(
            [
                ["Trying again later", "Resource ready"],
                ["Resource ready"], 
                ["Trying again later", "Resource ready"]
            ], dataset["Content"]
        )
        self.assertListEqual(
            [
                ["Trying again later", "Resource ready"],
                ["Resource ready"], 
                ["Trying again later", "Resource ready"]
            ], dataset["Template"]
        )
        self.assertListEqual([[0, 1], [1], [0, 1]], dataset["Event ID"])
        self.assertListEqual([[1.], [], [1.]], dataset["Time Diff"])