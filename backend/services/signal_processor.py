"""Signal Processor — Layer 1: Constructs feature vector from raw signals."""
import numpy as np
from services.sentiment_analyzer import SentimentService

sentiment_service = SentimentService()

# Store interaction history per session
session_history: dict[str, list] = {}


def process_signal(
    session_id: str,
    response_delay_ms: float,
    reedit_count: int,
    raw_text: str,
    expected_word_count: int,
    error_type: str,
) -> dict:
    """Process raw signals into feature vector x_t ∈ ℝ⁸."""

    # Δt — response delay
    delta_t = response_delay_ms

    # fr — re-edit frequency
    f_r = reedit_count

    # Sw — word sentiment score
    s_w = sentiment_service.analyze(raw_text)

    # Br — answer brevity ratio
    actual_words = len(raw_text.split()) if raw_text.strip() else 0
    b_r = actual_words / max(expected_word_count, 1)

    # E — error pattern vector (4D: conceptual, careless, repeated, novel)
    error_map = {
        "conceptual": [1.0, 0.0, 0.0, 0.0],
        "careless": [0.0, 1.0, 0.0, 0.0],
        "repeated": [0.0, 0.0, 1.0, 0.0],
        "novel": [0.0, 0.0, 0.0, 1.0],
        "none": [0.0, 0.0, 0.0, 0.0],
    }
    e_vec = error_map.get(error_type, [0.0, 0.0, 0.0, 0.0])

    # Construct feature vector x_t = [Δt, fr, Sw, Br, E₁, E₂, E₃, E₄] ∈ ℝ⁸
    feature_vector = [delta_t, f_r, s_w, b_r] + e_vec

    # Store in session history for temporal analysis
    if session_id not in session_history:
        session_history[session_id] = []
    session_history[session_id].append(feature_vector)

    # Keep last 50 interactions
    if len(session_history[session_id]) > 50:
        session_history[session_id] = session_history[session_id][-50:]

    return {
        "feature_vector": feature_vector,
        "metrics": {
            "response_latency": round(delta_t, 1),
            "friction_events": f_r,
            "sentiment_polarity": s_w,
            "brevity_ratio": round(b_r, 2),
            "error_type": error_type,
        },
    }


def get_session_history(session_id: str) -> list:
    """Get temporal history of feature vectors for a session."""
    return session_history.get(session_id, [])


def get_interaction_count(session_id: str) -> int:
    return len(session_history.get(session_id, []))
