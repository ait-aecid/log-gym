
from backbone.parser import ParserMethods, Parser

import unittest


logs = [
    "INFO:root:[2024-10-28/11:49:32] INFO:Standard Resource ready",
    "INFO:root:[2024-10-28/11:49:32] TRACE:Standard Process has ended",
    "INFO:root:[2024-10-28/11:49:32] TRACE:Standard Process has started ok",
]


structured_logs = {
    "Level": ["INFO", "TRACE", "TRACE"],
    "Module": ["Standard", "Standard", "Standard"],
    "Date": ["2024-10-28", "2024-10-28", "2024-10-28"],
    "Time": ["11:49:32", "11:49:32", "11:49:32"],
    "Content": [
        "Resource ready",
        "Process has ended",
        "Process has started ok"
    ],
    "Template": [
        "Resource ready",
        "Process has<*>",
        "Process has<*><*>" 
    ],
    "Event ID": [0, 1, 2]
}


structured_logs_output = {
    "Level": ["INFO", "TRACE", "TRACE"],
    "Module": ["Standard", "Standard", "Standard"],
    "Date": ["2024-10-28", "2024-10-28", "2024-10-28"],
    "Time": ["11:49:32", "11:49:32", "11:49:32"],
    "Content": [
        "Resource ready",
        "Process has ended",
        "Process has started ok"
    ],
    "Template": [
        "Resource ready",
        "Process has<*>",
        "Process has<*><*>" 
    ],
    "Event ID": [0, 2, 1],
    "Variables": [[], ["ended"], ["started", "ok"]]
}


logs_cients = [
    "INFO:root:[2024-10-28/11:49:32] INFO:Standard <*Client_1*>Resource ready",
    "INFO:root:[2024-10-28/11:49:32] TRACE:Standard <*Client_2*>Process has ended",
    "INFO:root:[2024-10-28/11:49:32] TRACE:Standard <*Client_1*>Process has started ok",
]


class ParserMethodsTestCase(unittest.TestCase):
    def test_unformat_logs(self) -> None:
        structured_logs = ParserMethods.structure_logs(logs)
        expected = {
            "Level": ["INFO", "TRACE", "TRACE"],
            "Module": ["Standard", "Standard", "Standard"],
            "Date": ["2024-10-28", "2024-10-28", "2024-10-28"],
            "Time": ["11:49:32", "11:49:32", "11:49:32"],
            "Content": [
                "Resource ready",
                "Process has ended",
                "Process has started ok"
            ]
        }
        self.assertDictEqual(structured_logs, expected)

    def test_unformat_logs_with_clients(self) -> None:
        structured_logs = ParserMethods.structure_logs(logs_cients)
        expected = {
            "Level": ["INFO", "TRACE", "TRACE"],
            "Client": [1, 2, 1],
            "Module": ["Standard", "Standard", "Standard"],
            "Date": ["2024-10-28", "2024-10-28", "2024-10-28"],
            "Time": ["11:49:32", "11:49:32", "11:49:32"],
            "Content": [
                "Resource ready",
                "Process has ended",
                "Process has started ok"
            ]
        }
        print(structured_logs)
        self.assertDictEqual(structured_logs, expected)

    def test_get_variables(self) -> None:
        structured_logs_ = ParserMethods.get_variables(structured_logs)
        variables = structured_logs_["Variables"]
        expected = [[], ["ended"], ["started", "ok"]]
        
        self.assertEqual(len(variables), len(expected))
        for var, exp in zip(variables, expected):
            self.assertListEqual(var, exp) 


class ParserTestcase(unittest.TestCase):
    def test_log_parser_templates(self) -> None:
        parser = Parser.from_file("test/logs_tests/messages.yaml") 
        templates = parser(logs)["Templates"]
        expected = {
            "Event ID": [0, 1, 2] ,
            "Template":[      
                "Resource ready",
                "Process has<*>",
                "Process has<*><*>" 
            ]
        }

        self.assertSetEqual(
            set(expected["Event ID"]), set(templates["Event ID"].tolist())
        )
        self.assertSetEqual(
            set(expected["Template"]), set(templates["Template"].tolist())
        )

    def test_log_parser_structured_logs(self) -> None:
        parser = Parser.from_file("test/logs_tests/messages.yaml") 
        structured_logs_ = parser(logs)["Structured logs"]
        result = structured_logs_.to_dict("list")

        self.assertSetEqual(
            set(result["Event ID"]), set(structured_logs_output["Event ID"])
        )
        expected = structured_logs_output.copy()
        del expected["Event ID"]
        del result["Event ID"]
        self.assertDictEqual(result, expected)

    def test_log_parser_structured_logs_clients(self) -> None:
        parser = Parser.from_file("test/logs_tests/messages.yaml") 
        structured_logs_ = parser(logs_cients)["Structured logs"]
        result = structured_logs_.to_dict("list")

        self.assertSetEqual(
            set(result["Event ID"]), set(structured_logs_output["Event ID"])
        )
        expected = structured_logs_output.copy()
        expected["Client"] = [1, 2, 1]
        del expected["Event ID"]
        del result["Event ID"]
        self.assertDictEqual(result, expected)

    def test_log_parser_templates_from_file(self) -> None:
        parser = Parser.from_file("test/logs_tests/messages.yaml") 
        templates = parser.load_logs(
            "test/logs_tests/test_logs.log"
        )["Templates"]
        expected = {
            "Event ID": [0, 1, 2] ,
            "Template":[      
                "Resource ready",
                "Process has<*>",
                "Process has<*><*>" 
            ]
        }

        self.assertSetEqual(
            set(expected["Event ID"]), set(templates["Event ID"].tolist())
        )
        self.assertSetEqual(
            set(expected["Template"]), set(templates["Template"].tolist())
        )

    def test_log_parser_structured_logs_clients_from_file(self) -> None:
        parser = Parser.from_file("test/logs_tests/messages.yaml") 
        structured_logs_ = parser.load_logs(
            "test/logs_tests/test_logs_clients.log"
        )["Structured logs"]
        result = structured_logs_.to_dict("list")

        self.assertSetEqual(
            set(result["Event ID"]), set(structured_logs_output["Event ID"])
        )
        expected = structured_logs_output.copy()
        expected["Client"] = [1, 2, 1]
        del expected["Event ID"]
        del result["Event ID"]
        self.assertDictEqual(result, expected)