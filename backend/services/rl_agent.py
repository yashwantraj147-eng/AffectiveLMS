"""Contextual Bandit RL Agent — Layer 3: Thompson Sampling.

Selects optimal (topic, difficulty, modality) action given emotional state.
Uses Beta-distributed priors for exploration-exploitation balance.
"""
import numpy as np
from collections import defaultdict

DIFFICULTIES = ["foundational", "basic", "intermediate", "advanced", "expert"]
MODALITIES = ["text", "video", "quiz"]

# Thompson Sampling parameters: Beta(alpha, beta) for each (state, action) pair
# alpha = successes + 1, beta = failures + 1
_bandit_params: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(lambda: [1.0, 1.0]))

# Initialize with informed priors (from the paper's pedagogical rules)
INFORMED_PRIORS = {
    "Confused": {
        "difficulty_down": [5, 1],    # Simplify: high success
        "modality_video": [4, 1],     # Switch to video: good
        "modality_text": [1, 3],      # Keep text: bad
        "revisit": [4, 1],            # Revisit prerequisite: good
        "maintain": [1, 4],           # Stay same: bad
    },
    "Frustrated": {
        "difficulty_down": [4, 1],
        "modality_quiz": [3, 2],      # Gamified quiz
        "modality_video": [4, 1],     # Video: good
        "modality_text": [1, 3],
        "maintain": [1, 5],
    },
    "Fatigued": {
        "difficulty_down": [3, 1],
        "modality_video": [4, 1],     # Less effort
        "modality_quiz": [3, 2],      # Interactive
        "modality_text": [1, 4],      # More effort: bad
        "maintain": [1, 3],
    },
    "Engaged": {
        "maintain": [5, 1],           # Stay the course
        "difficulty_up": [2, 2],      # Slight challenge
        "modality_text": [3, 1],
        "modality_video": [2, 2],
        "modality_quiz": [2, 2],
    },
    "Flow-state": {
        "difficulty_up": [5, 1],      # Challenge them
        "advance_topic": [4, 1],      # Move forward
        "maintain": [2, 2],
        "modality_quiz": [3, 1],      # Test knowledge
        "modality_text": [3, 1],
    },
}

# Load priors
for state, actions in INFORMED_PRIORS.items():
    for action, params in actions.items():
        _bandit_params[state][action] = params.copy()


def _thompson_sample(state: str) -> str:
    """Sample from Beta distributions to select best action."""
    actions = _bandit_params[state]
    if not actions:
        return "maintain"

    best_action = None
    best_sample = -1

    for action, (alpha, beta) in actions.items():
        sample = np.random.beta(alpha, beta)
        if sample > best_sample:
            best_sample = sample
            best_action = action

    return best_action or "maintain"


def get_adaptation(
    emotional_state: str,
    current_topic: str,
    current_difficulty: str,
    current_modality: str,
    topics: list,
) -> dict:
    """Select optimal pedagogical intervention via Thompson Sampling."""

    action = _thompson_sample(emotional_state)

    # Map abstract action to concrete (topic, difficulty, modality)
    new_topic = current_topic
    new_difficulty = current_difficulty
    new_modality = current_modality
    reason = ""
    action_type = "maintain"

    diff_idx = DIFFICULTIES.index(current_difficulty) if current_difficulty in DIFFICULTIES else 1

    if action == "difficulty_down" and diff_idx > 0:
        new_difficulty = DIFFICULTIES[diff_idx - 1]
        reason = f"Detected {emotional_state} state. Reducing difficulty from {current_difficulty} to {new_difficulty} for better comprehension."
        action_type = "simplify"

    elif action == "difficulty_up" and diff_idx < len(DIFFICULTIES) - 1:
        new_difficulty = DIFFICULTIES[diff_idx + 1]
        reason = f"Student is in {emotional_state}! Increasing challenge from {current_difficulty} to {new_difficulty}."
        action_type = "escalate"

    elif action.startswith("modality_"):
        new_modality = action.replace("modality_", "")
        reason = f"Switching content mode to {new_modality} to better suit {emotional_state} state."
        action_type = "switch_modality"

    elif action == "revisit":
        # Find prerequisite topic
        topic_ids = [t["id"] for t in topics]
        if current_topic in topic_ids:
            topic_obj = next(t for t in topics if t["id"] == current_topic)
            if topic_obj.get("prerequisites"):
                new_topic = topic_obj["prerequisites"][0]
                new_difficulty = "basic"
                reason = f"Student appears {emotional_state}. Revisiting prerequisite topic for reinforcement."
                action_type = "revisit"
            else:
                new_difficulty = DIFFICULTIES[max(0, diff_idx - 1)]
                reason = f"Simplifying current topic due to {emotional_state} state."
                action_type = "simplify"

    elif action == "advance_topic":
        topic_ids = [t["id"] for t in topics]
        if current_topic in topic_ids:
            curr_idx = topic_ids.index(current_topic)
            if curr_idx < len(topics) - 1:
                new_topic = topic_ids[curr_idx + 1]
                reason = f"Student in {emotional_state}! Advancing to next topic."
                action_type = "escalate"
            else:
                new_difficulty = DIFFICULTIES[min(len(DIFFICULTIES) - 1, diff_idx + 1)]
                reason = f"Completed all topics! Increasing difficulty."
                action_type = "escalate"

    elif action == "maintain":
        reason = f"Student is {emotional_state}. Maintaining current learning path."
        action_type = "maintain"

    # Find topic title
    topic_title = current_topic
    for t in topics:
        if t["id"] == new_topic:
            topic_title = t["title"]
            break

    return {
        "topic": new_topic,
        "topic_title": topic_title,
        "difficulty": new_difficulty,
        "modality": new_modality,
        "reason": reason,
        "action_type": action_type,
        "rl_action": action,
    }


def update_reward(emotional_state: str, action: str, reward: float):
    """Update bandit parameters based on observed reward."""
    if action in _bandit_params[emotional_state]:
        if reward > 0:
            _bandit_params[emotional_state][action][0] += 1  # success
        else:
            _bandit_params[emotional_state][action][1] += 1  # failure
