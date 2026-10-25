import unittest

from utils import parse_llm_response


class ParseLLMResponseTest(unittest.TestCase):
    def test_plain_json(self):
        result = parse_llm_response(
            '{"vulnerable": true, "type": "SQLi", "confidence": 0.9, "reason": "x"}'
        )
        self.assertTrue(result["vulnerable"])
        self.assertEqual(result["type"], "SQLi")
        self.assertEqual(result["confidence"], 0.9)

    def test_markdown_wrapped_json(self):
        result = parse_llm_response(
            '```json\n{"vulnerable": true, "type": "SQLi"}\n```'
        )
        self.assertTrue(result["vulnerable"])
        self.assertEqual(result["type"], "SQLi")

    def test_invalid_json_returns_defaults(self):
        result = parse_llm_response("not json")
        self.assertFalse(result["vulnerable"])
        self.assertEqual(result["type"], "None")
        self.assertEqual(result["confidence"], 0.0)

    def test_missing_keys_return_defaults(self):
        result = parse_llm_response("{}")
        self.assertFalse(result["vulnerable"])
        self.assertEqual(result["type"], "None")
        self.assertEqual(result["reason"], "")

    def test_confidence_clamped(self):
        result = parse_llm_response('{"confidence": 5}')
        self.assertEqual(result["confidence"], 1.0)

    def test_string_false(self):
        result = parse_llm_response('{"vulnerable": "false"}')
        self.assertFalse(result["vulnerable"])

    def test_none_input(self):
        result = parse_llm_response(None)
        self.assertFalse(result["vulnerable"])


if __name__ == "__main__":
    unittest.main()
