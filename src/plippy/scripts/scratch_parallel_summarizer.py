from __future__ import annotations

import asyncio
import json
from pathlib import Path


# Practice goal:
# 1) Read 4 JSON files in parallel.
# 2) Build one summary per file.
# 3) Build a combined summary across all files.


async def read_text_async(path: Path) -> str:
    # Hint: asyncio.to_thread keeps file I/O off the event loop.
    return await asyncio.to_thread(path.read_text, encoding="utf-8")


def clean_text(value: str) -> str:
    # Hint: replace this with your own string-normalization pipeline.
    return " ".join(value.split()).strip().lower()


async def summarize_file(path: Path) -> dict[str, object]:
    raw = await read_text_async(path)
    payload = json.loads(raw)

    source = str(payload.get("source", "unknown"))
    records = payload.get("records", [])
    if not isinstance(records, list):
        raise ValueError(f"Expected records list in {path.name}")

    cleaned = []
    for row in records:
        if not isinstance(row, dict):
            continue
        text = clean_text(str(row.get("text", "")))
        cleaned.append(text)

    # TODO: expand this summary with metrics you want to practice.
    # Ideas:
    # - average score
    # - max/min text length
    # - word frequency map
    # - count of records containing certain keywords
    summary = {
        "file": path.name,
        "source": source,
        "record_count": len(records),
        "non_empty_text_count": sum(1 for t in cleaned if t),
        "total_text_chars": sum(len(t) for t in cleaned),
    }
    return summary


def summarize_all(file_summaries: list[dict[str, object]]) -> dict[str, object]:
    # TODO: customize this combined summary for your own practice.
    total_files = len(file_summaries)
    total_records = sum(int(s.get("record_count", 0)) for s in file_summaries)
    total_chars = sum(int(s.get("total_text_chars", 0)) for s in file_summaries)

    return {
        "total_files": total_files,
        "total_records": total_records,
        "total_text_chars": total_chars,
    }


async def main() -> None:
    scripts_dir = Path(__file__).resolve().parent
    inputs_dir = scripts_dir / "scratch_inputs"

    # Keep this explicit list while practicing, then try auto-discovery with glob later.
    input_paths = [
        inputs_dir / "input_1.json",
        inputs_dir / "input_2.json",
        inputs_dir / "input_3.json",
        inputs_dir / "input_4.json",
    ]

    # Parallel read + summarize.
    per_file = await asyncio.gather(*(summarize_file(path) for path in input_paths))
    combined = summarize_all(per_file)

    print("Per-file summaries:")
    print(json.dumps(per_file, indent=2))

    print("\nCombined summary:")
    print(json.dumps(combined, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
