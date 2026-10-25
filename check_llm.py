from config import create_client
from parser import extract_functions
from test_llm import analyze_function
from utils import parse_llm_response

client = create_client()

funcs = extract_functions("test_code.py")

for f in funcs:
    print(f"=== {f['name']} ===")
    result_text = analyze_function(f["code"], client)

    result = parse_llm_response(result_text)

    print(f"Vulnerable: {result['vulnerable']}")
    print(f"Type: {result['type']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Reason: {result['reason']}")
    print()
