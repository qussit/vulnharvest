from openai import OpenAI
from parser import extract_functions
from test_llm import analyze_function

client = OpenAI(
    base_url="http://localhost:11434/v1/",
    api_key="ollama",
)

funcs = extract_functions("test_code.py")

for f in funcs:
    print(f"=== {f['name']} ===")
    result = analyze_function(f["code"], client)
    print(result)
    print()