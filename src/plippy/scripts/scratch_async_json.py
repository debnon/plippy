from __future__ import annotations

import asyncio
import json
from pathlib import Path


SAMPLE_DATA = {
    "users": [
        {
            "id": 1,
            "name": "  Alice Johnson  ",
            "email": "ALICE@example.com",
            "bio": "Loves Python, APIs, and   clean code.",
        },
        {
            "id": 2,
            "name": "bob smith",
            "email": " Bob.Smith@Example.COM ",
            "bio": "Enjoys async io + data pipelines!",
        },
        {
            "id": 3,
            "name": "  ChloE   Nguyen",
            "email": "chloe.nguyen@example.com",
            "bio": "Writes tests; fixes bugs; ships features.",
        },
    ]
}


def ensure_sample_file(path: Path) -> None:
    """Create a sample JSON file if it does not already exist."""
    if path.exists():
        return
    path.write_text(json.dumps(SAMPLE_DATA, indent=2), encoding="utf-8")


async def read_text_async(path: Path) -> str:
    """Read file content in a thread so the event loop stays responsive."""
    return await asyncio.to_thread(path.read_text, encoding="utf-8")


def normalize_space(text: str) -> str:
    """Collapse repeated whitespace and trim edges."""
    return " ".join(text.split())


def transform_user(user: dict[str, object]) -> dict[str, object]:
    name = normalize_space(str(user.get("name", ""))).title()
    email = normalize_space(str(user.get("email", ""))).lower()
    bio = normalize_space(str(user.get("bio", "")))

    words = [w.strip(".,;:!?+").lower() for w in bio.split()]
    unique_word_count = len({w for w in words if w})

    return {
        "id": user.get("id"),
        "name": name,
        "email": email,
        "bio": bio,
        "bio_word_count": len(words),
        "bio_unique_word_count": unique_word_count,
    }


async def enrich_user(user: dict[str, object]) -> dict[str, object]:
    """Pretend to do async I/O while transforming data."""
    await asyncio.sleep(0.15)
    return transform_user(user)


async def main() -> None:
    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / "scratch_input.json"

    ensure_sample_file(input_path)

    raw_text = await read_text_async(input_path)
    payload = json.loads(raw_text)

    users = payload.get("users", [])
    if not isinstance(users, list):
        raise ValueError("Expected 'users' to be a list in scratch_input.json")

    print(f"Read {len(users)} users from {input_path.name}\n")

    transformed = await asyncio.gather(*(enrich_user(u) for u in users if isinstance(u, dict)))

    print("Transformed users:")
    print(json.dumps(transformed, indent=2))

    csv_preview_lines = ["id,name,email,bio_word_count,bio_unique_word_count"]
    for row in transformed:
        csv_preview_lines.append(
            f"{row['id']},{row['name']},{row['email']},{row['bio_word_count']},{row['bio_unique_word_count']}"
        )

    print("\nCSV preview (string manipulation output):")
    print("\n".join(csv_preview_lines))


if __name__ == "__main__":
    asyncio.run(main())
