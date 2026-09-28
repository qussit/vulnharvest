from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1/",
    api_key="ollama",
)

response = client.chat.completions.create(
    model="qwen3:8b",
    messages=[
        {"role": "system", "content": "Ты эксперт по безопасности приложений."},
        {"role": "user", "content": "Что такое SQL-инъекция? Ответь одним предложением."},
    ]
)

print("=== ПОЛНЫЙ ОТВЕТ ===")
print(response)
print()
print("=== CONTENT ===")
print(repr(response.choices[0].message.content))