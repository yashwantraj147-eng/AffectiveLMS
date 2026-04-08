"""VADER Sentiment Analyzer — Layer 1 component."""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentService:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> float:
        """Return compound sentiment score in range [-1.0, +1.0]."""
        if not text or not text.strip():
            return 0.0
        scores = self.analyzer.polarity_scores(text)
        return round(scores["compound"], 3)
