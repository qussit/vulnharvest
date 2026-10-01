import json
import re


def parse_llm_response(text):
    """Извлекает JSON из ответа модели, даже если он обёрнут в markdown."""
    match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        json_text = match.group(1)
    else:
        json_text = text
    return json.loads(json_text.strip())