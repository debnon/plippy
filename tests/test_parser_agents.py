import asyncio
from pathlib import Path
from types import TracebackType
from typing import Any

import pytest
from pypdf import PdfWriter

from plippy.agents.base import AgentContext
from plippy.agents.pdf import PdfExtractAgent
from plippy.agents.web import WebFetchAgent


class _DummyResponse:
    def __init__(self, text: str, status_code: int = 200) -> None:
        self.text = text
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError("HTTP error")


class _DummyClient:
    def __init__(self, text: str) -> None:
        self._text = text

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool:
        _ = (exc_type, exc, tb)
        return False

    async def get(self, url: str):
        _ = url
        return _DummyResponse(self._text)


def test_web_fetch_agent_extracts_title_and_text(monkeypatch: pytest.MonkeyPatch) -> None:
    html = "<html><head><title>Doc</title></head><body><h1>Hello</h1><p>world</p></body></html>"

    def _client_factory(*args: Any, **kwargs: Any) -> _DummyClient:
        _ = (args, kwargs)
        return _DummyClient(html)

    monkeypatch.setattr("plippy.agents.web.httpx.AsyncClient", _client_factory)

    agent = WebFetchAgent()
    result = asyncio.run(agent.run({"url": "https://example.com"}, AgentContext(results={})))

    assert result.output["title"] == "Doc"
    assert "Hello world" in result.output["text"]


def test_pdf_extract_agent_reads_local_pdf(tmp_path: Path) -> None:
    pdf_path = tmp_path / "sample.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with pdf_path.open("wb") as file_obj:
        writer.write(file_obj)

    agent = PdfExtractAgent()
    result = asyncio.run(
        agent.run({"path": str(pdf_path), "allowed_root": str(tmp_path)}, AgentContext(results={}))
    )

    assert result.output["pages"] == 1
    assert "text" in result.output
