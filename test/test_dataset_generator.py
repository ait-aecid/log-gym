import dataset_generator as dg

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


class DataGeneratorTestCase(unittest.TestCase):
    def test_split_process(self):
        gen = dg.split_in_process(pd.read_csv("test/logs_tests/structured_logs.csv"))
        expected = [first_expected, second_expected, third_expected]
        for z, table in enumerate(gen):
            table_ = table.to_dict("list")
            for k in table_.keys():
                self.assertListEqual(expected[z][k], table_[k])
        self.assertEqual(2, z)
