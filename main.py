import os
import argparse
import json

from config import create_client
from analyzer import analyze_file

# Папки, которые не нужно сканировать при обходе каталогов.
EXCLUDED_DIRS = {".venv", ".git", "__pycache__", "site-packages"}


def collect_results(path, client, model=None):
    """Собирает результаты анализа файла или папки."""
    results = []

    if os.path.isfile(path):
        results.extend(analyze_file(path, client, model=model))
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    results.extend(analyze_file(full_path, client, model=model))

    return results


def is_visible(result, min_confidence):
    """Результат показывается, если есть ошибка или уверенность не ниже порога."""
    return result["error"] is not None or result["confidence"] >= min_confidence


def print_text(results, min_confidence):
    current_file = None
    for r in results:
        if r["file"] != current_file:
            current_file = r["file"]
            print(f"\n### Файл: {current_file} ###\n")

        if r["error"]:
            print(f"[{r['error']}]")
            continue

        if r["confidence"] < min_confidence:
            print(
                f"=== {r['function']} === "
                f"[низкая уверенность {r['confidence']:.2f} < {min_confidence}, пропущено]"
            )
            continue

        print(f"=== {r['function']} ===")
        print(f"Vulnerable: {r['vulnerable']}")
        print(f"Type: {r['type']}")
        print(f"Confidence: {r['confidence']}")
        print(f"Reason: {r['reason']}")
        print()


def print_json(results, min_confidence):
    visible = [r for r in results if is_visible(r, min_confidence)]
    print(json.dumps(visible, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="VulnHarvest — LLM-powered vulnerability scanner")
    parser.add_argument("path", help="Файл или папка для анализа")
    parser.add_argument(
        "--model",
        default=None,
        help="Модель Ollama (по умолчанию VULNHARVEST_MODEL или qwen3:8b)",
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.0,
        help="Порог уверенности (0.0–1.0), ниже которого результат скрывается",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Формат вывода (text или json)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Путь не существует: {args.path}")
        return

    client = create_client()
    results = collect_results(args.path, client, model=args.model)

    if args.format == "json":
        print_json(results, args.min_confidence)
    else:
        print_text(results, args.min_confidence)


if __name__ == "__main__":
    main()
