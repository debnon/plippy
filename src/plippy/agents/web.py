from __future__ import annotations

import os
from typing import Any
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from plippy.agents.base import AgentContext, AgentResult


class WebFetchAgent:
    async def run(self, payload: dict[str, Any], context: AgentContext) -> AgentResult:
        _ = context

        url = str(payload.get("url", "")).strip()
        if not url:
            raise ValueError("web_fetch requires 'url'")

        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("web_fetch only supports http/https URLs")

        allowed_hosts = [h.strip() for h in os.getenv("PLIPPY_ALLOWED_WEB_HOSTS", "").split(",") if h.strip()]
        if allowed_hosts and parsed.hostname not in set(allowed_hosts):
            raise ValueError("hostname is not in PLIPPY_ALLOWED_WEB_HOSTS")

        timeout_seconds = float(payload.get("timeout_seconds", 10))
        max_chars = int(payload.get("max_chars", 40000))

        async with httpx.AsyncClient(timeout=timeout_seconds, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        title = (soup.title.string.strip() if soup.title and soup.title.string else "")
        text = " ".join(soup.get_text(separator=" ").split())
        if len(text) > max_chars:
            text = text[:max_chars]

        return AgentResult(
            output={
                "url": url,
                "status_code": response.status_code,
                "title": title,
                "text": text,
            }
        )
