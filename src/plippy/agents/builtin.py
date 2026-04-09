from __future__ import annotations

from typing import Any

from plippy.agents.base import Agent, AgentContext, AgentResult
from plippy.agents.pdf import PdfExtractAgent
from plippy.agents.web import WebFetchAgent


class EchoAgent:
    async def run(self, payload: dict[str, Any], context: AgentContext) -> AgentResult:
        _ = context
        return AgentResult(output={"text": str(payload.get("text", "")), "payload": payload})


class JoinAgent:
    async def run(self, payload: dict[str, Any], context: AgentContext) -> AgentResult:
        task_ids = payload.get("task_ids", [])
        separator = str(payload.get("separator", "\n"))
        parts: list[str] = []
        for task_id in task_ids:
            task_result = context.results.get(str(task_id), {})
            output = task_result.get("output", {})
            if "text" in output:
                parts.append(str(output["text"]))
            else:
                parts.append(str(output))
        return AgentResult(output={"text": separator.join(parts)})


class TemplateAgent:
    async def run(self, payload: dict[str, Any], context: AgentContext) -> AgentResult:
        template = str(payload.get("template", ""))
        rendered = template
        for task_id, task_result in context.results.items():
            output = task_result.get("output", {})
            if "text" in output:
                rendered = rendered.replace(f"{{{{{task_id}.text}}}}", str(output["text"]))
            rendered = rendered.replace(f"{{{{{task_id}.output}}}}", str(output))
        return AgentResult(output={"text": rendered})


DEFAULT_AGENT_REGISTRY: dict[str, Agent] = {
    "echo": EchoAgent(),
    "join": JoinAgent(),
    "template": TemplateAgent(),
    "web_fetch": WebFetchAgent(),
    "pdf_extract": PdfExtractAgent(),
}
