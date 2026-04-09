from __future__ import annotations

import io
import os
from pathlib import Path
from typing import Any

import httpx
from pypdf import PdfReader

from plippy.agents.base import AgentContext, AgentResult


class PdfExtractAgent:
    async def run(self, payload: dict[str, Any], context: AgentContext) -> AgentResult:
        _ = context

        if "path" in payload:
            return self._from_path(payload)
        if "url" in payload:
            return await self._from_url(payload)

        raise ValueError("pdf_extract requires either 'path' or 'url'")

    def _from_path(self, payload: dict[str, Any]) -> AgentResult:
        path_value = str(payload.get("path", "")).strip()
        if not path_value:
            raise ValueError("pdf_extract path cannot be empty")

        pdf_path = Path(path_value).resolve()
        allowed_root = Path(str(payload.get("allowed_root", os.getenv("PLIPPY_PDF_ROOT", "/app")))).resolve()
        if not pdf_path.is_relative_to(allowed_root):
            raise ValueError("pdf path is outside allowed root")

        if not pdf_path.exists() or not pdf_path.is_file():
            raise ValueError("pdf file does not exist")

        reader = PdfReader(str(pdf_path))
        pages_text = [(page.extract_text() or "") for page in reader.pages]
        text = "\n".join(pages_text)
        return AgentResult(output={"path": str(pdf_path), "pages": len(reader.pages), "text": text})

    async def _from_url(self, payload: dict[str, Any]) -> AgentResult:
        url = str(payload.get("url", "")).strip()
        if not url:
            raise ValueError("pdf_extract url cannot be empty")

        timeout_seconds = float(payload.get("timeout_seconds", 15))
        max_bytes = int(payload.get("max_bytes", 10_000_000))

        async with httpx.AsyncClient(timeout=timeout_seconds, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.content

        if len(data) > max_bytes:
            raise ValueError("pdf payload exceeds max_bytes")

        reader = PdfReader(io.BytesIO(data))
        pages_text = [(page.extract_text() or "") for page in reader.pages]
        text = "\n".join(pages_text)
        return AgentResult(output={"url": url, "pages": len(reader.pages), "text": text})
