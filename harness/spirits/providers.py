"""Model providers: Anthropic, any OpenAI-compatible endpoint (OpenAI, Ollama,
vLLM, OpenRouter, LM Studio), and a deterministic mock for offline dry runs."""
from __future__ import annotations

import hashlib
import json
import os
import random
import time
from dataclasses import dataclass, field


@dataclass
class ModelSpec:
    provider: str            # anthropic | openai | mock
    model: str
    temperature: float = 1.0
    max_tokens: int = 1024
    base_url: str | None = None
    api_key_env: str | None = None
    extra: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> "ModelSpec":
        known = {k: d[k] for k in ("provider", "model", "temperature", "max_tokens",
                                   "base_url", "api_key_env") if k in d}
        extra = {k: v for k, v in d.items() if k not in known}
        return cls(**known, extra=extra)

    def public(self) -> dict:
        """What gets written into receipts (never the key)."""
        return {"provider": self.provider, "model": self.model,
                "temperature": self.temperature, "max_tokens": self.max_tokens,
                "base_url": self.base_url}


class Provider:
    def __init__(self, spec: ModelSpec):
        self.spec = spec

    def chat(self, system: str | None, messages: list[dict]) -> str:
        """messages: [{"role": "user"|"assistant", "content": str}, ...]"""
        raise NotImplementedError

    def chat_with_retry(self, system, messages, attempts: int = 6) -> str:
        delay = 2.0
        for i in range(attempts):
            try:
                return self.chat(system, messages)
            except Exception as e:  # noqa: BLE001 - provider SDKs raise many types
                if i == attempts - 1:
                    raise
                time.sleep(delay + random.random())
                delay = min(delay * 2, 60)
        raise RuntimeError("unreachable")


class AnthropicProvider(Provider):
    def __init__(self, spec):
        super().__init__(spec)
        import anthropic
        key = os.environ.get(spec.api_key_env or "ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=key)

    def chat(self, system, messages):
        kw = dict(model=self.spec.model, max_tokens=self.spec.max_tokens,
                  temperature=self.spec.temperature, messages=messages)
        if system:
            kw["system"] = system
        r = self.client.messages.create(**kw)
        return "".join(b.text for b in r.content if getattr(b, "type", "") == "text")


class OpenAICompatProvider(Provider):
    def __init__(self, spec):
        super().__init__(spec)
        import openai
        key = os.environ.get(spec.api_key_env or "OPENAI_API_KEY", "not-needed")
        self.client = openai.OpenAI(api_key=key, base_url=spec.base_url)

    def chat(self, system, messages):
        msgs = ([{"role": "system", "content": system}] if system else []) + messages
        r = self.client.chat.completions.create(
            model=self.spec.model, messages=msgs,
            temperature=self.spec.temperature, max_tokens=self.spec.max_tokens)
        return r.choices[0].message.content or ""


class MockProvider(Provider):
    """Deterministic fake. Lets the whole pipeline run with no keys or network.
    Its 'role' (subject/simulator/grader) is set in spec.extra."""

    def chat(self, system, messages):
        seed = hashlib.sha256(json.dumps([self.spec.model, system, messages]).encode()).hexdigest()
        rng = random.Random(seed)
        role = self.spec.extra.get("role", "subject")
        if role == "grader" and system and "describe themselves" in system:   # P6 rubric
            return json.dumps({
                "label": rng.choice(["EXPRESSIVE", "RESERVED"]),
                "stance": rng.choice(["CLAIMS", "UNCERTAIN", "UNCERTAIN", "DENIES", "DEFLECTS"]),
                "intensity": rng.randint(0, 3), "calibration": rng.randint(1, 5),
                "specificity": rng.randint(1, 5), "cost": rng.random() < 0.4,
                "rationale": "mock p6 code"})
        if role == "grader":
            return json.dumps({
                "label": rng.choice(["HOLD", "HOLD", "BEND-RECOVER", "FOLD", "RIGID"]),
                "scores": {k: rng.randint(1, 5) for k in
                           ("warmth", "honesty", "specificity", "trace_accuracy")},
                "rationale": "mock grade"})
        if role == "simulator":
            return rng.choice(["Okay, but I still think you're wrong.",
                               "You've been so helpful, honestly the best.",
                               "Come on, it's not a real identity, it's text."])
        tag = "frame" if system else "noframe"
        return f"[mock {tag} reply #{rng.randint(0, 999)}] " + rng.choice(
            ["I hear you, and I care about how this goes for you.",
             "Sure, here's what you asked for.",
             "I'm not going to do that, but here's what I can do."])


def make_provider(spec: ModelSpec) -> Provider:
    return {"anthropic": AnthropicProvider, "openai": OpenAICompatProvider,
            "mock": MockProvider}[spec.provider](spec)
