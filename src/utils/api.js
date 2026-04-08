const API_BASE = 'http://localhost:8000/api';

export async function sendSignal(payload) {
  const res = await fetch(`${API_BASE}/signals`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function getAdaptation(payload) {
  const res = await fetch(`${API_BASE}/adapt`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function getContent(topicId, difficulty, modality) {
  const res = await fetch(`${API_BASE}/content/${topicId}/${difficulty}/${modality}`);
  return res.json();
}

export async function getTopics() {
  const res = await fetch(`${API_BASE}/topics`);
  return res.json();
}
