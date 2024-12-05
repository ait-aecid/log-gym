
from msg_reader import Messages

import unittest


msgs = {
    "message_1": {
        "v1": "hello there",
        "v1_template": "hello <*>",
        "v2": "general kenobi",
        "v2_template": "general <*>"
    },
    "message_2": {
        "v2": "general kenobi",
        "v2_template": "general <*>"
    }
}


class MessagesTestCase(unittest.TestCase):
    def test_two_versions_msg(self) -> None:
        msgs1 = Messages(msgs=msgs, version=1)
        msgs2 = Messages(msgs=msgs, version=2)

        self.assertEqual("hello there", msgs1["message_1"])
        self.assertEqual("hello there", msgs1.message_1)
        self.assertEqual("general kenobi", msgs2["message_1"])
        self.assertEqual("general kenobi", msgs2.message_1)

    def test_two_versions_templates(self) -> None:
        msgs1 = Messages(msgs=msgs, version=1)
        msgs2 = Messages(msgs=msgs, version=2)

        self.assertEqual("hello <*>", msgs1.templates["message_1"])
        self.assertEqual("hello <*>", msgs1.templates.message_1)
        self.assertEqual("general <*>", msgs2.templates["message_1"])
        self.assertEqual("general <*>", msgs2.templates.message_1)

    def test_two_versions_msg_none(self) -> None:
        msgs1 = Messages(msgs=msgs, version=1)
        msgs2 = Messages(msgs=msgs, version=2)

        self.assertEqual(None, msgs1["message_2"])
        self.assertEqual(None, msgs1.message_2)
        self.assertEqual("general kenobi", msgs2["message_2"])
        self.assertEqual("general kenobi", msgs2.message_2)

    def test_two_versions_templates_none(self) -> None:
        msgs1 = Messages(msgs=msgs, version=1)
        msgs2 = Messages(msgs=msgs, version=2)

        self.assertEqual(None, msgs1.templates["message_2"])
        self.assertEqual(None, msgs1.templates.message_2)
        self.assertEqual("general <*>", msgs2.templates["message_2"])
        self.assertEqual("general <*>", msgs2.templates.message_2)

    def test_from_file(self) -> None:
        path = "test/logs_tests/msgs_test.yaml"
        msgs1 = Messages.from_file(path, version=1)
        msgs2 = Messages.from_file(path, version=2)

        self.assertEqual(None, msgs1["message_2"])
        self.assertEqual(None, msgs1.message_2)
        self.assertEqual("general kenobi", msgs2["message_2"])
        self.assertEqual("general kenobi", msgs2.message_2)
        self.assertEqual(None, msgs1.templates["message_2"])
        self.assertEqual(None, msgs1.templates.message_2)
        self.assertEqual("general <*>", msgs2.templates["message_2"])
        self.assertEqual("general <*>", msgs2.templates.message_2)