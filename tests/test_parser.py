import os
import tempfile
import unittest

from parser import extract_functions


class ExtractFunctionsTest(unittest.TestCase):
    def _extract(self, source):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "sample.py")
            with open(path, "w", encoding="utf-8") as f:
                f.write(source)
            return extract_functions(path)

    def test_top_level_functions(self):
        funcs = self._extract("""
def foo(a):
    return a

def bar(b):
    return b
""")
        self.assertEqual([f["name"] for f in funcs], ["foo", "bar"])

    def test_nested_function_not_duplicated(self):
        funcs = self._extract("""
def outer():
    def inner():
        pass
    return inner
""")
        self.assertEqual([f["name"] for f in funcs], ["outer"])

    def test_async_function(self):
        funcs = self._extract("""
async def fetch(url):
    return url
""")
        self.assertEqual([f["name"] for f in funcs], ["fetch"])

    def test_methods_in_class(self):
        funcs = self._extract("""
class Handler:
    def get(self):
        return 1

    async def post(self):
        return 2
""")
        self.assertEqual([f["name"] for f in funcs], ["get", "post"])

    def test_code_field_contains_body(self):
        funcs = self._extract("""
def foo(a):
    return a
""")
        self.assertIn("return a", funcs[0]["code"])


if __name__ == "__main__":
    unittest.main()
