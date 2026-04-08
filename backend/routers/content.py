"""Content Router — Serve learning content from curriculum."""
import json
import os
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Load curriculum
CURRICULUM_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "curriculum.json")
with open(CURRICULUM_PATH, "r", encoding="utf-8") as f:
    CURRICULUM = json.load(f)

TOPICS = CURRICULUM["topics"]


@router.get("/content/{topic_id}/{difficulty}/{modality}")
def get_content(topic_id: str, difficulty: str, modality: str):
    """Fetch specific content by topic, difficulty, and modality."""
    topic = next((t for t in TOPICS if t["id"] == topic_id), None)
    if not topic:
        raise HTTPException(status_code=404, detail=f"Topic '{topic_id}' not found")

    content = topic.get("content", {}).get(difficulty)
    if not content:
        raise HTTPException(status_code=404, detail=f"Difficulty '{difficulty}' not found for topic '{topic_id}'")

    return {
        "topic_id": topic_id,
        "topic_title": topic["title"],
        "difficulty": difficulty,
        "modality": modality,
        "content": content.get(modality, content.get("text", "")),
        "all_content": content,
    }


@router.get("/topics")
def list_topics():
    """List all available topics."""
    return [
        {
            "id": t["id"],
            "title": t["title"],
            "prerequisites": t.get("prerequisites", []),
            "order": t.get("order", 0),
        }
        for t in TOPICS
    ]


@router.get("/curriculum")
def get_curriculum():
    """Get full curriculum data."""
    return CURRICULUM
