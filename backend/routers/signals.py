"""Signals Router — Ingest behavioural data and return emotion classification."""
from fastapi import APIRouter
from models.schemas import SignalPayload, EmotionStateResponse
from services.signal_processor import process_signal, get_interaction_count
from services.emotion_classifier import classify_emotion

router = APIRouter()

# In-memory session states
_session_states: dict[str, dict] = {}


@router.post("/signals", response_model=EmotionStateResponse)
def ingest_signal(payload: SignalPayload):
    """Layer 1 → Layer 2: Process signal and classify emotion."""

    # Layer 1: Process raw signals into feature vector
    result = process_signal(
        session_id=payload.session_id,
        response_delay_ms=payload.response_delay_ms,
        reedit_count=payload.reedit_count,
        raw_text=payload.raw_text,
        expected_word_count=payload.expected_word_count,
        error_type=payload.error_type,
    )

    # Layer 2: Classify emotional state
    classification = classify_emotion(
        session_id=payload.session_id,
        current_features=result["feature_vector"],
    )

    # Store session state
    _session_states[payload.session_id] = {
        "emotional_state": classification["emotional_state"],
        "metrics": result["metrics"],
        "focus_density": classification["focus_density"],
    }

    return EmotionStateResponse(
        session_id=payload.session_id,
        emotional_state=classification["emotional_state"],
        confidence=classification["confidence"],
        metrics=result["metrics"],
        focus_density=classification["focus_density"],
        interaction_count=get_interaction_count(payload.session_id),
    )


@router.get("/state/{session_id}")
def get_state(session_id: str):
    """Get current emotional state for a session."""
    if session_id in _session_states:
        return _session_states[session_id]
    return {
        "emotional_state": "Engaged",
        "metrics": {
            "response_latency": 0,
            "friction_events": 0,
            "sentiment_polarity": 0.0,
            "brevity_ratio": 0,
        },
        "focus_density": 0,
    }
