import argparse
from openai import OpenAI
from parser import extract_functions
from test_llm import analyze_function
from utils import parse_llm_response


def main():
    parser = argparse.ArgumentParser(description="VulnHarvest — LLM-powered vulnerability scanner")
    parser.add_argument("path", help="Файл или папка для анализа")
    args = parser.parse_args()
    
    client = OpenAI(
        base_url="http://localhost:11434/v1/",
        api_key="ollama",
    )
    
    funcs = extract_functions(args.path)
    
    for f in funcs:
        print(f"=== {f['name']} ===")
        result_text = analyze_function(f["code"], client)
        result = parse_llm_response(result_text)
        print(f"Vulnerable: {result['vulnerable']}")
        print(f"Type: {result['type']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Reason: {result['reason']}")
        print()


if __name__ == "__main__":
    main()