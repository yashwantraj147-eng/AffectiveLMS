"""Pydantic schemas for request/response models."""
from pydantic import BaseModel
from typing import Optional


class SignalPayload(BaseModel):
    session_id: str
    response_delay_ms: float  # Δt
    reedit_count: int  # fr
    raw_text: str  # for sentiment analysis
    expected_word_count: int
    error_type: str  # conceptual | careless | repeated | novel | none
    timestamp: float


class EmotionStateResponse(BaseModel):
    session_id: str
    emotional_state: str  # Engaged | Fatigued | Confused | Frustrated | Flow-state
    confidence: float
    metrics: dict  # response_latency, friction_events, sentiment, brevity_ratio
    focus_density: float
    interaction_count: int


class AdaptationRequest(BaseModel):
    session_id: str
    current_topic: str
    current_difficulty: str
    current_modality: str


class AdaptationResponse(BaseModel):
    topic: str
    topic_title: str
    difficulty: str
    modality: str
    reason: str
    action_type: str  # maintain | escalate | simplify | switch_modality | revisit


class ContentRequest(BaseModel):
    topic: str
    difficulty: str
    modality: str


class SessionResponse(BaseModel):
    session_id: str
    emotional_state: str
    current_topic: str
    current_difficulty: str
    current_modality: str
