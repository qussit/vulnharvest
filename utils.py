import json
import re

DEFAULT_RESULT = {
    "vulnerable": False,
    "type": "None",
    "confidence": 0.0,
    "reason": "",
}


def parse_llm_response(text):
    """Извлекает JSON из ответа модели и приводит его к безопасному виду.

    Никогда не бросает исключение: при ошибке парсинга или неполном JSON
    возвращает значения по умолчанию. confidence нормализуется в диапазон [0, 1].
    """
    result = dict(DEFAULT_RESULT)
    if not text:
        return result

    match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    json_text = match.group(1) if match else text

    try:
        data = json.loads(json_text.strip())
    except (json.JSONDecodeError, AttributeError, TypeError):
        return result

    if not isinstance(data, dict):
        return result

    result["vulnerable"] = _to_bool(data.get("vulnerable"))
    result["type"] = _to_str(data.get("type"), "None")
    result["confidence"] = _to_confidence(data.get("confidence"))
    result["reason"] = _to_str(data.get("reason"), "")

    return result


def _to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes")
    return bool(value)


def _to_str(value, default):
    if value is None:
        return default
    return str(value)


def _to_confidence(value):
    try:
        conf = float(value)
    except (TypeError, ValueError):
        return DEFAULT_RESULT["confidence"]
    return max(0.0, min(1.0, conf))
