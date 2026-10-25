import os
import argparse

from config import create_client
from parser import extract_functions
from test_llm import analyze_function
from utils import parse_llm_response

# Папки, которые не нужно сканировать при обходе каталогов.
EXCLUDED_DIRS = {".venv", ".git", "__pycache__", "site-packages"}


def analyze_file(filepath, client, model=None):
    """Анализирует один файл и печатает результат."""
    print(f"\n### Файл: {filepath} ###\n")

    try:
        funcs = extract_functions(filepath)
    except Exception as e:
        print(f"[пропущен] Не удалось разобрать файл: {e}")
        return

    for f in funcs:
        print(f"=== {f['name']} ===")
        try:
            result_text = analyze_function(f["code"], client, model=model)
            result = parse_llm_response(result_text)
            print(f"Vulnerable: {result['vulnerable']}")
            print(f"Type: {result['type']}")
            print(f"Confidence: {result['confidence']}")
            print(f"Reason: {result['reason']}")
        except Exception as e:
            print(f"[ошибка] Не удалось проанализировать функцию: {e}")
        print()


def main():
    parser = argparse.ArgumentParser(description="VulnHarvest — LLM-powered vulnerability scanner")
    parser.add_argument("path", help="Файл или папка для анализа")
    parser.add_argument(
        "--model",
        default=None,
        help="Модель Ollama (по умолчанию берётся из VULNHARVEST_MODEL или qwen3:8b)",
    )
    args = parser.parse_args()

    client = create_client()

    if os.path.isfile(args.path):
        analyze_file(args.path, client, model=args.model)
    elif os.path.isdir(args.path):
        for root, dirs, files in os.walk(args.path):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    analyze_file(full_path, client, model=args.model)
    else:
        print(f"Путь не существует: {args.path}")


if __name__ == "__main__":
    main()
