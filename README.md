# VulnHarvest

LLM-powered vulnerability scanner · Сканер уязвимостей на основе LLM (Ollama)

> Выберите язык · Choose language

<details open>
<summary>🇷🇺 Русский</summary>

Сканер уязвимостей на основе LLM (Ollama). Разбирает Python-файлы через AST,
извлекает функции и анализирует каждую на наличие уязвимостей
(SQL-инъекции, path traversal, command injection) с помощью локальной модели.

## Возможности

- Анализ одного файла или целой папки (рекурсивно, только `.py`).
- Извлечение функций через `ast`: функции верхнего уровня, методы классов и `async`-функции.
- Защита от prompt injection: код оборачивается в ограничители и трактуется как данные.
- Нормализация ответа модели — результат всегда валидный, падений нет.
- Порог уверенности (`--min-confidence`) и два формата вывода (`text`, `json`).
- Таймауты и повторные попытки запросов к Ollama.

## Требования

- Python 3.14+
- Запущенный [Ollama](https://ollama.com) с моделью `qwen3:8b` (по умолчанию).

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Использование

```bash
# один файл
python main.py test_code.py

# папка (рекурсивно; .venv, .git, __pycache__, site-packages пропускаются)
python main.py .

# JSON-вывод и порог уверенности
python main.py . --format json --min-confidence 0.7

# другая модель
python main.py . --model dolphin-mistral:latest
```

## Конфигурация

Переменные окружения (все необязательные):

| Переменная | По умолчанию | Описание |
|------------|--------------|----------|
| `VULNHARVEST_BASE_URL` | `http://localhost:11434/v1/` | адрес Ollama |
| `VULNHARVEST_API_KEY` | `ollama` | API-ключ |
| `VULNHARVEST_MODEL` | `qwen3:8b` | имя модели |
| `VULNHARVEST_TIMEOUT` | `120` | таймаут запроса, секунды |
| `VULNHARVEST_MAX_RETRIES` | `2` | число повторных попыток |

## Структура проекта

| Файл | Назначение |
|------|-----------|
| `main.py` | CLI-точка входа |
| `analyzer.py` | общая логика анализа файла |
| `parser.py` | извлечение функций через AST |
| `test_llm.py` | промпт и вызов LLM |
| `utils.py` | парсинг/нормализация JSON-ответа |
| `config.py` | конфигурация |
| `check_llm.py` | отладочный прогон `test_code.py` |
| `test_code.py` | примеры функций для проверки |

## Тесты

```bash
python -m unittest discover -s tests -t .
```

## Ограничения

- Результаты зависят от LLM и недетерминированы; защита от prompt injection
  не является строгой гарантией.
- Анализируются только функции верхнего уровня: вложенные функции попадают
  в код родителя и отдельно не анализируются.
- Вывод JSON — плоский список; экспорт SARIF не реализован.

</details>

<details>
<summary>🇬🇧 English</summary>

An LLM-powered vulnerability scanner (Ollama). Parses Python files via AST,
extracts functions, and analyzes each one for vulnerabilities
(SQL injection, path traversal, command injection) using a local model.

## Features

- Analyze a single file or a whole directory (recursively, `.py` only).
- Function extraction via `ast`: top-level functions, class methods, and `async` functions.
- Prompt injection protection: code is wrapped in delimiters and treated as data.
- Response normalization — the result is always valid and never crashes.
- Confidence threshold (`--min-confidence`) and two output formats (`text`, `json`).
- Timeouts and retries for Ollama requests.

## Requirements

- Python 3.14+
- A running [Ollama](https://ollama.com) with the `qwen3:8b` model (default).

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# single file
python main.py test_code.py

# directory (recursive; .venv, .git, __pycache__, site-packages are skipped)
python main.py .

# JSON output with a confidence threshold
python main.py . --format json --min-confidence 0.7

# another model
python main.py . --model dolphin-mistral:latest
```

## Configuration

Environment variables (all optional):

| Variable | Default | Description |
|----------|---------|-------------|
| `VULNHARVEST_BASE_URL` | `http://localhost:11434/v1/` | Ollama address |
| `VULNHARVEST_API_KEY` | `ollama` | API key |
| `VULNHARVEST_MODEL` | `qwen3:8b` | model name |
| `VULNHARVEST_TIMEOUT` | `120` | request timeout, seconds |
| `VULNHARVEST_MAX_RETRIES` | `2` | number of retries |

## Project structure

| File | Purpose |
|------|---------|
| `main.py` | CLI entry point |
| `analyzer.py` | shared file-analysis logic |
| `parser.py` | function extraction via AST |
| `test_llm.py` | prompt and LLM call |
| `utils.py` | response parsing/normalization |
| `config.py` | configuration |
| `check_llm.py` | debug run over `test_code.py` |
| `test_code.py` | sample functions for testing |

## Tests

```bash
python -m unittest discover -s tests -t .
```

## Limitations

- Results depend on the LLM and are non-deterministic; prompt-injection protection
  is not a strict guarantee.
- Only top-level functions are analyzed: nested functions are included in the
  parent's code and not analyzed separately.
- JSON output is a flat list; SARIF export is not implemented.

</details>
