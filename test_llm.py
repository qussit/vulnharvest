from openai import OpenAI


def analyze_function(code, client):
    system_prompt = """Ты эксперт по безопасности приложений. Проанализируй Python-функцию на наличие уязвимостей (SQL-инъекции, path traversal, command injection).

Верни ответ СТРОГО в формате JSON, без markdown, без пояснений:
{
  "vulnerable": true или false,
  "type": "SQLi" или "PathTraversal" или "CommandInjection" или "None",
  "confidence": число от 0.0 до 1.0,
  "reason": "краткое объяснение"
}"""

    response = client.chat.completions.create(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Проанализируй функцию:\n\n{code}"},
        ]
    )
    return response.choices[0].message.content