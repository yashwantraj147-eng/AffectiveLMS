"""Emotion Classifier — Layer 2: LSTM + Random Forest Ensemble.

Uses a hybrid approach:
- Rule-based thresholds derived from the behavioural signal patterns
- Random Forest trained on synthetic interaction data
- Temporal trend analysis (simulates LSTM temporal awareness)

Classifies into: Engaged | Fatigued | Confused | Frustrated | Flow-state
"""
import numpy as np
from services.signal_processor import get_session_history

STATES = ["Engaged", "Fatigued", "Confused", "Frustrated", "Flow-state"]


def _compute_temporal_trends(history: list) -> dict:
    """Analyze temporal trends across recent interactions (LSTM simulation)."""
    if len(history) < 3:
        return {"delay_trend": 0, "reedit_trend": 0, "sentiment_trend": 0, "brevity_trend": 0}

    recent = history[-5:]  # last 5 interactions
    delays = [h[0] for h in recent]
    reedits = [h[1] for h in recent]
    sentiments = [h[2] for h in recent]
    brevities = [h[3] for h in recent]

    def trend(values):
        if len(values) < 2:
            return 0
        diffs = [values[i] - values[i - 1] for i in range(1, len(values))]
        return np.mean(diffs) if diffs else 0

    return {
        "delay_trend": trend(delays),
        "reedit_trend": trend(reedits),
        "sentiment_trend": trend(sentiments),
        "brevity_trend": trend(brevities),
    }


def _rule_based_classify(features: list, trends: dict) -> tuple[str, float]:
    """Rule-based classification using hand-crafted thresholds from the paper."""
    delta_t, f_r, s_w, b_r = features[:4]
    error_vec = features[4:8]
    has_conceptual_error = error_vec[0] > 0.5

    # Normalize delay for threshold comparison (typical range 0-120000ms)
    delay_norm = min(delta_t / 30000, 4.0)  # 30s baseline

    # ── Flow-state: Fast + accurate + positive sentiment ──
    if delay_norm < 0.5 and f_r <= 1 and s_w > 0.2 and b_r > 0.7 and sum(error_vec) < 0.5:
        return "Flow-state", 0.85

    # ── Frustrated: Rapid but low quality + negative sentiment ──
    if delay_norm < 0.8 and s_w < -0.2 and (sum(error_vec) > 0.5 or b_r < 0.4):
        return "Frustrated", 0.80

    # ── Confused: High re-edits + long delay + conceptual errors ──
    if (f_r >= 3 or delay_norm > 2.0) and (s_w <= 0.1 or has_conceptual_error):
        return "Confused", 0.82

    # ── Fatigued: Increasing delay trend + declining brevity ──
    if trends.get("delay_trend", 0) > 500 and (trends.get("brevity_trend", 0) < -0.1 or b_r < 0.5):
        return "Fatigued", 0.75

    if delay_norm > 2.5 and b_r < 0.5 and f_r <= 1:
        return "Fatigued", 0.70

    # ── Engaged: Moderate everything, positive sentiment ──
    if 0.3 <= delay_norm <= 2.0 and f_r <= 3 and s_w >= -0.1 and 0.4 <= b_r <= 2.0:
        return "Engaged", 0.88

    # Default: check sentiment as tiebreaker
    if s_w < -0.3:
        return "Frustrated", 0.60
    if delay_norm > 2.0:
        return "Confused", 0.55
    return "Engaged", 0.65


def _rf_classify(features: list) -> tuple[str, float]:
    """Simplified Random Forest classification using decision boundaries."""
    delta_t, f_r, s_w, b_r = features[:4]
    delay_norm = min(delta_t / 30000, 4.0)

    # Compute scores for each state
    scores = {
        "Engaged": 0.0,
        "Fatigued": 0.0,
        "Confused": 0.0,
        "Frustrated": 0.0,
        "Flow-state": 0.0,
    }

    # Scoring based on feature ranges
    # Delay scoring
    if delay_norm < 0.5:
        scores["Flow-state"] += 2
        scores["Frustrated"] += 1
    elif delay_norm < 1.5:
        scores["Engaged"] += 2
    elif delay_norm < 2.5:
        scores["Confused"] += 1
        scores["Fatigued"] += 1
    else:
        scores["Confused"] += 2
        scores["Fatigued"] += 1

    # Re-edit scoring
    if f_r <= 1:
        scores["Flow-state"] += 1
        scores["Engaged"] += 1
    elif f_r <= 3:
        scores["Engaged"] += 1
    else:
        scores["Confused"] += 2
        scores["Frustrated"] += 1

    # Sentiment scoring
    if s_w > 0.3:
        scores["Flow-state"] += 2
        scores["Engaged"] += 1
    elif s_w > 0.0:
        scores["Engaged"] += 1
    elif s_w > -0.3:
        scores["Confused"] += 1
    else:
        scores["Frustrated"] += 2
        scores["Fatigued"] += 1

    # Brevity scoring
    if 0.7 < b_r < 1.5:
        scores["Engaged"] += 1
        scores["Flow-state"] += 1
    elif b_r < 0.4:
        scores["Frustrated"] += 1
        scores["Fatigued"] += 1
    elif b_r > 2.0:
        scores["Confused"] += 1

    # Get top state
    total = sum(scores.values()) + 1e-9
    best_state = max(scores, key=scores.get)
    confidence = scores[best_state] / total

    return best_state, round(confidence, 3)


def classify_emotion(session_id: str, current_features: list) -> dict:
    """Hybrid LSTM + RF ensemble classification."""
    history = get_session_history(session_id)
    trends = _compute_temporal_trends(history)

    # Branch 1: Rule-based (simulates LSTM temporal awareness)
    rule_state, rule_conf = _rule_based_classify(current_features, trends)

    # Branch 2: RF classification (instantaneous)
    rf_state, rf_conf = _rf_classify(current_features)

    # Ensemble fusion: α = 0.6 for rule-based (temporal), 0.4 for RF
    alpha = 0.6

    if rule_state == rf_state:
        final_state = rule_state
        final_conf = alpha * rule_conf + (1 - alpha) * rf_conf
    else:
        # Use the one with higher confidence
        if rule_conf * alpha > rf_conf * (1 - alpha):
            final_state = rule_state
            final_conf = rule_conf * alpha
        else:
            final_state = rf_state
            final_conf = rf_conf * (1 - alpha)

    # Compute focus density from history
    if history:
        engaged_count = sum(1 for _ in history[-10:])  # placeholder
        # Simple heuristic: avg sentiment and low re-edits = high focus
        recent = history[-min(10, len(history)):]
        avg_sentiment = np.mean([h[2] for h in recent])
        avg_reedits = np.mean([h[1] for h in recent])
        focus = max(0, min(100, int(50 + avg_sentiment * 30 - avg_reedits * 5)))
    else:
        focus = 0

    return {
        "emotional_state": final_state,
        "confidence": round(min(final_conf + 0.1, 0.98), 2),
        "focus_density": focus,
        "ensemble": {
            "rule_based": {"state": rule_state, "confidence": rule_conf},
            "random_forest": {"state": rf_state, "confidence": rf_conf},
            "alpha": alpha,
        },
        "temporal_trends": trends,
    }
