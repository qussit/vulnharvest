"""Общая логика анализа файлов.

Переиспользуется из main.py (CLI) и check_llm.py (отладка).
"""
from parser import extract_functions
from test_llm import analyze_function
from utils import parse_llm_response


def analyze_file(filepath, client, model=None):
    """Анализирует один файл и возвращает список результатов.

    Каждый элемент — dict с ключами:
      file, function, vulnerable, type, confidence, reason, error.
    """
    results = []

    try:
        funcs = extract_functions(filepath)
    except Exception as e:
        return [{
            "file": filepath,
            "function": None,
            "vulnerable": False,
            "type": "None",
            "confidence": 0.0,
            "reason": "",
            "error": f"Не удалось разобрать файл: {e}",
        }]

    for f in funcs:
        entry = {
            "file": filepath,
            "function": f["name"],
            "vulnerable": False,
            "type": "None",
            "confidence": 0.0,
            "reason": "",
            "error": None,
        }
        try:
            result_text = analyze_function(f["code"], client, model=model)
            result = parse_llm_response(result_text)
            entry.update(
                vulnerable=result["vulnerable"],
                type=result["type"],
                confidence=result["confidence"],
                reason=result["reason"],
            )
        except Exception as e:
            entry["error"] = f"Не удалось проанализировать функцию: {e}"

        results.append(entry)

    return results
