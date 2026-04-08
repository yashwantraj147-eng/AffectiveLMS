# 🧠 AffectiveLMS

**Emotion-Aware Adaptive Learning Path Generator Using Behavioural Signal Analysis**

> A zero-hardware, privacy-preserving adaptive learning system that infers student emotional states from text-based behavioural signals and dynamically adapts content delivery using reinforcement learning.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-8.0-646CFF?style=flat-square&logo=vite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🎯 What Is This?

AffectiveLMS is a working prototype of an **emotion-aware learning management system** that:

1. **Passively captures behavioural signals** (response delay, re-edit frequency, word sentiment, answer brevity) — using **zero hardware** (no camera, no sensors, no biometrics)
2. **Classifies emotional state** (Engaged / Confused / Frustrated / Fatigued / Flow-state) using an **LSTM + Random Forest ensemble**
3. **Dynamically adapts the learning path** (topic, difficulty, content modality) using a **Contextual Bandit RL agent** with Thompson Sampling

All of this happens in **real-time**, within a **privacy-preserving** architecture compliant with GDPR, FERPA, and India's DPDP Act 2023.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   AffectiveLMS Frontend                  │
│                                                          │
│  ┌──────────────┐  ┌───────────────┐  ┌───────────────┐ │
│  │ Content Card  │  │  Input Panel  │  │  Analytics    │ │
│  │ (text/video/  │  │  (signal      │  │  Panel        │ │
│  │  quiz)        │  │   capture)    │  │  (dashboard)  │ │
│  └──────┬───────┘  └──────┬────────┘  └───────────────┘ │
│         │                 │                              │
│         │    useSignalCapture Hook                       │
│         │    (Δt, fr, Sw, Br, E)                        │
└─────────┼─────────────────┼──────────────────────────────┘
          │                 │
          ▼                 ▼
┌─────────────────────────────────────────────────────────┐
│                   FastAPI Backend                        │
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │ Layer 1:     │  │ Layer 2:     │  │ Layer 3:       │ │
│  │ Signal       │→ │ LSTM + RF    │→ │ Contextual     │ │
│  │ Processor    │  │ Ensemble     │  │ Bandit RL      │ │
│  │              │  │ Classifier   │  │ (Thompson      │ │
│  │ Feature      │  │              │  │  Sampling)     │ │
│  │ Vector x∈ℝ⁸ │  │ 5 States     │  │ Adapt Path     │ │
│  └─────────────┘  └──────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.10+

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/AffectiveLMS.git
cd AffectiveLMS
```

### 2. Start the Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Backend runs on `http://localhost:8000` — API docs at `http://localhost:8000/docs`

### 3. Start the Frontend
```bash
cd ..  # back to project root
npm install
npm run dev
```
Frontend runs on `http://localhost:5173`

### 4. Use the App
1. Open `http://localhost:5173` in your browser
2. Read the AI curriculum content displayed
3. Type your response in the input area
4. Hit **Submit Response** or press Enter
5. Watch the system:
   - Capture your behavioural signals (Δt, re-edits, sentiment)
   - Classify your emotional state
   - Adapt the content if needed (difficulty, modality, topic)

---

## 📊 Behavioural Signals Captured

| Signal | Symbol | Description | Capture Method |
|--------|--------|-------------|----------------|
| Response Delay | Δt | Milliseconds from question display to first keystroke | JS `keydown` listeners |
| Re-edit Frequency | f_r | Count of backspace/delete/cut events | DOM event tracking |
| Word Sentiment | S_w | Sentiment polarity score (-1.0 to +1.0) | VADER NLP |
| Answer Brevity | B_r | Ratio of response length to expected length | Server computation |
| Error Pattern | E | 4D error type distribution vector | Rule-based analysis |

---

## 🎭 Emotional States

| State | Signal Pattern | System Response |
|-------|---------------|-----------------|
| **Engaged** | Moderate Δt, consistent Br≈1, positive Sw | Maintain current path |
| **Confused** | High fr, long Δt, negative Sw, conceptual errors | Simplify, revisit prerequisites |
| **Frustrated** | Rapid but low-quality, negative Sw | Switch modality, lower difficulty |
| **Fatigued** | Increasing Δt over time, declining Br | Reduce load, offer break |
| **Flow-state** | Fast + accurate, positive Sw, minimal fr | Challenge with harder material |

---

## 🔬 ML Pipeline

### Layer 2: Emotion Classification
- **VADER Sentiment Analysis** for real-time text polarity
- **LSTM Branch** (temporal patterns across session)
- **Random Forest Branch** (instantaneous feature snapshot)
- **Ensemble Fusion**: `p_final = α·p_LSTM + (1-α)·p_RF`

### Layer 3: Contextual Bandit RL
- **Thompson Sampling** with Beta-distributed priors
- **Action Space**: topic × difficulty × modality
- **Reward**: +1 (state improves), 0 (unchanged), -1 (deteriorates)
- Informed priors from pedagogical research

---

## 📁 Project Structure

```
AffectiveLMS/
├── index.html              # Entry point
├── vite.config.js          # Vite + React config
├── package.json
├── src/
│   ├── main.jsx            # React mount
│   ├── App.jsx             # Main app orchestrator
│   ├── App.css             # Component styles
│   ├── index.css           # Design system
│   ├── components/
│   │   ├── Header.jsx          # Brand header + signal status
│   │   ├── ContentCard.jsx     # Text/video/quiz content display
│   │   ├── InputPanel.jsx      # Student input + signal capture
│   │   ├── AnalyticsPanel.jsx  # Affective Analytics dashboard
│   │   ├── PipelineIndicator.jsx # 3-stage pipeline footer
│   │   └── CognitiveAlert.jsx  # Adaptation notification
│   ├── hooks/
│   │   └── useSignalCapture.js # Core signal capture engine
│   └── utils/
│       ├── api.js              # Backend API client
│       └── constants.js        # Emotion colors, difficulties
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── requirements.txt
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   ├── services/
│   │   ├── signal_processor.py # Layer 1: Feature vector
│   │   ├── sentiment_analyzer.py # VADER sentiment
│   │   ├── emotion_classifier.py # Layer 2: LSTM+RF ensemble
│   │   └── rl_agent.py         # Layer 3: Thompson Sampling
│   ├── routers/
│   │   ├── signals.py          # Signal ingestion API
│   │   ├── content.py          # Content serving API
│   │   └── adapt.py            # RL adaptation API
│   └── data/
│       └── curriculum.json     # AI curriculum + content
└── README.md
```

---

## 🛡️ Privacy

**Zero biometric data collected.** The system operates entirely on text-based interaction metadata:
- No camera or webcam access
- No microphone or voice data
- No wearable sensors
- No facial recognition
- No eye tracking

Compliant with: **GDPR**, **FERPA**, **COPPA**, **DPDP Act 2023 (India)**

---

## 📜 Curriculum

The demo includes a **Fundamentals of Artificial Intelligence** curriculum with 5 topics:
1. Introduction to Artificial Intelligence
2. Machine Learning Fundamentals
3. Neural Networks & Deep Learning
4. Natural Language Processing
5. Computer Vision

Each topic has 5 difficulty tiers (Foundational → Expert) and 3 content modalities (Text, Video, Quiz).

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React 19, Vite 8 |
| Backend | FastAPI (Python) |
| Sentiment Analysis | VADER |
| Classification | LSTM + Random Forest ensemble |
| RL Agent | Thompson Sampling Contextual Bandit |
| Styling | Vanilla CSS (dark glassmorphism) |

---

## 👥 Team

Built by Group 9, SCAI — VIT Bhopal University

| Name | Registration |
|------|-------------|
| Yashwant Raj | 24BCY10176 |
| Ankit Kumar | 24BCY10200 |
| Sohom Bose | 24BCY10172 |
| Deepayan Dey | 24BCY10068 |
| Kumari Garima | 24BCY10240 |
| Prakriti Verma | 24BHI10072 |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
