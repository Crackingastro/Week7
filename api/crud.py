import json
from pathlib import Path
from typing import List, Tuple

def get_top_products(
    conn,
    limit: int
) -> List[Tuple[str, int]]:
    """
    Query raw.raw_image_detections to find the most
    frequently detected object classes (excluding 'person').
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
              detected_object_class,
              COUNT(*) AS count
            FROM raw.raw_image_detections
            WHERE detected_object_class <> 'person'
            GROUP BY detected_object_class
            ORDER BY count DESC
            LIMIT %s
            """,
            (limit,)
        )
        return cur.fetchall()

def get_channel_folder_activity(
    root: Path
) -> List[Tuple[str, int]]:
    """
    Walk data/raw/telegram_messages/<date>/<channel>
    and count how many date-folders each channel appears in.
    Returns list of (channel_name, folder_count).
    """
    counts = {}
    for date_dir in root.iterdir():
        if not date_dir.is_dir():
            continue
        for channel_dir in date_dir.iterdir():
            if channel_dir.is_dir():
                counts[channel_dir.name] = counts.get(channel_dir.name, 0) + 1
    return list(counts.items())

def search_messages_fs(
    root: Path,
    query: str
) -> List[str]:
    """
    Walk data/raw/telegram_messages/<date>/<channel>/messages.json,
    load it, and return the full text of any message whose "text"
    contains `query` (case-insensitive).
    """
    results: List[str] = []
    for date_dir in root.iterdir():
        if not date_dir.is_dir():
            continue
        for channel_dir in date_dir.iterdir():
            if not channel_dir.is_dir():
                continue

            msg_file = channel_dir / "messages.json"
            if not msg_file.exists():
                continue

            data = json.loads(msg_file.read_text(encoding="utf-8"))
            for msg in data:
                text = msg.get("text", "")
                if query.lower() in text.lower():
                    results.append(text)
    return results
