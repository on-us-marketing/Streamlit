from __future__ import annotations

import os
import time
from typing import Any

from crewai.llms.base_llm import BaseLLM
from pydantic import PrivateAttr

from on_us_content_agent.llm_client import call_messages_api, response_text, usage


DEFAULT_API_URL = "https://devaicode.dev/v1/messages"


class AnthropicMessagesLLM(BaseLLM):
    """CrewAI-compatible LLM adapter for a Claude Messages-style endpoint.

    The current On-us testing endpoint uses a Claude `/v1/messages` style API.
    CrewAI normally routes through LiteLLM providers, which may expect a different
    provider format. This adapter keeps CrewAI as the orchestrator while using
    the same API call shape already tested in the earlier KB scripts.
    """

    provider: str = "on_us_messages_adapter"
    api_provider: str = "anthropic"
    _call_logs: list[dict[str, Any]] = PrivateAttr(default_factory=list)

    def call(
        self,
        messages: str | list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        callbacks: list[Any] | None = None,
        available_functions: dict[str, Any] | None = None,
        from_task: Any | None = None,
        from_agent: Any | None = None,
        response_model: Any | None = None,
    ) -> str:
        if tools:
            raise ValueError("Tool calling is not supported by AnthropicMessagesLLM in this POC.")
        if response_model is not None:
            raise ValueError("Structured response models are not supported by AnthropicMessagesLLM in this POC.")

        prompt = self._messages_to_prompt(messages)
        api_key = (
            self.api_key
            or os.getenv("LLM_API_KEY", "")
            or os.getenv("ANTHROPIC_API_KEY", "")
            or os.getenv("NVIDIA_API_KEY", "")
        ).strip()
        if not api_key:
            raise RuntimeError("Missing LLM_API_KEY, ANTHROPIC_API_KEY, or NVIDIA_API_KEY environment variable.")

        stage = getattr(from_task, "name", "") or "llm_call"
        agent_role = getattr(from_agent, "role", "") or "unknown_agent"
        start = time.perf_counter()
        response, elapsed = call_messages_api(
            api_key=api_key,
            api_url=self.base_url or os.getenv("LLM_API_URL", os.getenv("ANTHROPIC_API_URL", DEFAULT_API_URL)),
            model=self.model,
            prompt=prompt,
            max_tokens=int(self.max_tokens or 2000),
            temperature=float(self.temperature if self.temperature is not None else 0.2),
            provider=self.api_provider,
        )
        text = response_text(response)
        input_tokens, output_tokens = usage(response)
        total_tokens = input_tokens + output_tokens
        self._call_logs.append(
            {
                "stage": stage,
                "agent": agent_role,
                "provider": self.api_provider,
                "model": self.model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "time_seconds": round(elapsed or (time.perf_counter() - start), 2),
            }
        )
        self._track_token_usage_internal(
            {
                "prompt_tokens": input_tokens,
                "completion_tokens": output_tokens,
                "total_tokens": total_tokens,
                "successful_requests": 1,
            }
        )
        return text

    def call_logs(self) -> list[dict[str, Any]]:
        return list(self._call_logs)

    def _messages_to_prompt(self, messages: str | list[dict[str, Any]]) -> str:
        formatted = self._format_messages(messages)
        parts = []
        for msg in formatted:
            role = msg.get("role", "user")
            content = self._content_to_text(msg.get("content", ""))
            parts.append(f"{role.upper()}:\n{content}")
        return "\n\n".join(parts)

    def _content_to_text(self, content: Any) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        text_parts.append(str(item.get("text", "")))
                    else:
                        text_parts.append(str(item))
                else:
                    text_parts.append(str(item))
            return "\n".join(text_parts)
        return str(content)
