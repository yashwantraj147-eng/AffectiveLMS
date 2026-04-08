"""Adaptation Router — RL-based content recommendation."""
import json
import os
from fastapi import APIRouter
from models.schemas import AdaptationRequest, AdaptationResponse
from services.rl_agent import get_adaptation, update_reward

router = APIRouter()

CURRICULUM_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "curriculum.json")
with open(CURRICULUM_PATH, "r", encoding="utf-8") as f:
    TOPICS = json.load(f)["topics"]


@router.post("/adapt", response_model=AdaptationResponse)
def adapt_content(request: AdaptationRequest):
    """Layer 3: Get RL-recommended adaptation."""
    from routers.signals import _session_states

    state = _session_states.get(request.session_id, {})
    emotional_state = state.get("emotional_state", "Engaged")

    recommendation = get_adaptation(
        emotional_state=emotional_state,
        current_topic=request.current_topic,
        current_difficulty=request.current_difficulty,
        current_modality=request.current_modality,
        topics=TOPICS,
    )

    return AdaptationResponse(
        topic=recommendation["topic"],
        topic_title=recommendation["topic_title"],
        difficulty=recommendation["difficulty"],
        modality=recommendation["modality"],
        reason=recommendation["reason"],
        action_type=recommendation["action_type"],
    )


@router.post("/feedback")
def submit_feedback(session_id: str, action: str, reward: float, emotional_state: str):
    """Submit reward signal to update RL agent."""
    update_reward(emotional_state, action, reward)
    return {"status": "updated", "action": action, "reward": reward}
