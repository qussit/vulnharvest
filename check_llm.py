import json
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
    result_text = analyze_function(f["code"], client)
    
    result = json.loads(result_text)      # ← добавь эту строку
    
    print(f"Vulnerable: {result['vulnerable']}")
    print(f"Type: {result['type']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Reason: {result['reason']}")
    print()