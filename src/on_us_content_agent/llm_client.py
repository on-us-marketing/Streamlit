from __future__ import annotations

import json
import ssl
import time
import urllib.error
import urllib.request
from typing import Any


def certifi_cafile() -> str | None:
    try:
        import certifi

        return certifi.where()
    except Exception:
        return None


def normalize_provider(provider: str) -> str:
    value = (provider or "anthropic").strip().lower()
    if value in {"anthropic", "claude", "messages"}:
        return "anthropic"
    if value in {"openai", "chat", "chat_completions", "openai-compatible"}:
        return "openai"
    raise ValueError(f"Unsupported provider: {provider}")


def normalize_api_url(api_url: str, provider: str) -> str:
    url = api_url.rstrip("/")
    provider = normalize_provider(provider)
    if provider == "anthropic":
        return url if url.endswith("/messages") else f"{url}/v1/messages"
    if provider == "openai":
        return url if url.endswith("/chat/completions") else f"{url}/chat/completions"
    return url


def build_payload(*, provider: str, model: str, prompt: str, max_tokens: int, temperature: float) -> dict[str, Any]:
    provider = normalize_provider(provider)
    if provider == "anthropic":
        return {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
    return {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}],
    }


def build_headers(*, provider: str, api_key: str) -> dict[str, str]:
    provider = normalize_provider(provider)
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}",
        "user-agent": "On-us-Content-Agent-POC/0.1",
    }
    if provider == "anthropic":
        headers["x-api-key"] = api_key
        headers["anthropic-version"] = "2023-06-01"
    return headers


def call_messages_api(
    *,
    api_key: str,
    api_url: str,
    model: str,
    prompt: str,
    max_tokens: int,
    temperature: float,
    provider: str = "anthropic",
) -> tuple[dict[str, Any], float]:
    provider = normalize_provider(provider)
    payload = build_payload(
        provider=provider,
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        normalize_api_url(api_url, provider),
        data=data,
        method="POST",
        headers=build_headers(provider=provider, api_key=api_key),
    )
    context = ssl.create_default_context(cafile=certifi_cafile())
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=240, context=context) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{provider} API HTTP {exc.code}: {body}") from exc
    elapsed = time.perf_counter() - start
    return json.loads(body), elapsed


def response_text(response: dict[str, Any]) -> str:
    # Anthropic Messages API
    if isinstance(response.get("content"), list):
        text = "\n".join(
            item.get("text", "") for item in response.get("content", []) if item.get("type") == "text"
        ).strip()
        if text:
            return text

    # OpenAI-compatible chat completions
    choices = response.get("choices") or []
    if choices:
        message = choices[0].get("message") or {}
        content = message.get("content")
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            return "\n".join(
                item.get("text", "") if isinstance(item, dict) else str(item) for item in content
            ).strip()

    # Some hosted models may return text/output_text.
    for key in ("output_text", "text"):
        value = response.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    return ""


def usage(response: dict[str, Any]) -> tuple[int, int]:
    raw = response.get("usage", {})
    input_tokens = raw.get("input_tokens", raw.get("prompt_tokens", 0))
    output_tokens = raw.get("output_tokens", raw.get("completion_tokens", 0))
    return int(input_tokens or 0), int(output_tokens or 0)
