"""Конфигурация VulnHarvest.

Значения можно переопределить через переменные окружения:
  VULNHARVEST_BASE_URL    — адрес Ollama (по умолчанию http://localhost:11434/v1/)
  VULNHARVEST_API_KEY     — API-ключ (по умолчанию "ollama")
  VULNHARVEST_MODEL       — имя модели (по умолчанию "qwen3:8b")
  VULNHARVEST_TIMEOUT     — таймаут запроса в секундах (по умолчанию 120)
  VULNHARVEST_MAX_RETRIES — число повторных попыток (по умолчанию 2)
"""
import os

from openai import OpenAI

DEFAULT_BASE_URL = "http://localhost:11434/v1/"
DEFAULT_API_KEY = "ollama"
DEFAULT_MODEL = "qwen3:8b"
DEFAULT_TIMEOUT = 120.0
DEFAULT_MAX_RETRIES = 2


def get_base_url() -> str:
    return os.environ.get("VULNHARVEST_BASE_URL", DEFAULT_BASE_URL)


def get_api_key() -> str:
    return os.environ.get("VULNHARVEST_API_KEY", DEFAULT_API_KEY)


def get_model() -> str:
    return os.environ.get("VULNHARVEST_MODEL", DEFAULT_MODEL)


def get_timeout() -> float:
    try:
        return float(os.environ.get("VULNHARVEST_TIMEOUT", DEFAULT_TIMEOUT))
    except ValueError:
        return DEFAULT_TIMEOUT


def get_max_retries() -> int:
    try:
        return int(os.environ.get("VULNHARVEST_MAX_RETRIES", DEFAULT_MAX_RETRIES))
    except ValueError:
        return DEFAULT_MAX_RETRIES


def create_client() -> OpenAI:
    return OpenAI(
        base_url=get_base_url(),
        api_key=get_api_key(),
        timeout=get_timeout(),
        max_retries=get_max_retries(),
    )
