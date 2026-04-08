"""AffectiveLMS Backend — FastAPI Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import signals, content, adapt

app = FastAPI(
    title="AffectiveLMS API",
    description="Emotion-Aware Adaptive Learning Path Generator — Backend API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(signals.router, prefix="/api", tags=["Signals"])
app.include_router(content.router, prefix="/api", tags=["Content"])
app.include_router(adapt.router, prefix="/api", tags=["Adaptation"])


@app.get("/")
def root():
    return {
        "name": "AffectiveLMS API",
        "version": "1.0.0",
        "status": "running",
        "layers": [
            "Layer 1: Behavioural Signal Collection",
            "Layer 2: Emotion Classification (LSTM + RF Ensemble)",
            "Layer 3: Contextual Bandit RL Adaptation",
        ],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
