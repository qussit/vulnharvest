"""Конфигурация VulnHarvest.

Значения можно переопределить через переменные окружения:
  VULNHARVEST_BASE_URL  — адрес Ollama (по умолчанию http://localhost:11434/v1/)
  VULNHARVEST_API_KEY   — API-ключ (по умолчанию "ollama")
  VULNHARVEST_MODEL     — имя модели (по умолчанию "qwen3:8b")
"""
import os

from openai import OpenAI

DEFAULT_BASE_URL = "http://localhost:11434/v1/"
DEFAULT_API_KEY = "ollama"
DEFAULT_MODEL = "qwen3:8b"


def get_base_url() -> str:
    return os.environ.get("VULNHARVEST_BASE_URL", DEFAULT_BASE_URL)


def get_api_key() -> str:
    return os.environ.get("VULNHARVEST_API_KEY", DEFAULT_API_KEY)


def get_model() -> str:
    return os.environ.get("VULNHARVEST_MODEL", DEFAULT_MODEL)


def create_client() -> OpenAI:
    return OpenAI(
        base_url=get_base_url(),
        api_key=get_api_key(),
    )
