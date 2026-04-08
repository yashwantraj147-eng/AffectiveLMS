import { EMOTION_COLORS } from '../utils/constants';

export default function AnalyticsPanel({ emotionalState, confidence, metrics, focusDensity, interactionCount, liveMetrics }) {
  const emotionStyle = EMOTION_COLORS[emotionalState] || EMOTION_COLORS['Engaged'];

  const latency = metrics.response_latency || liveMetrics?.responseDelay || 0;
  const friction = metrics.friction_events || liveMetrics?.reeditCount || 0;
  const sentiment = metrics.sentiment_polarity || 0;

  const latencyBarWidth = Math.min((latency / 60000) * 100, 100);
  const frictionBarWidth = Math.min((friction / 10) * 100, 100);
  const sentimentBarWidth = ((sentiment + 1) / 2) * 100;

  return (
    <div className="analytics-panel">
      {/* Header */}
      <div className="analytics-header">
        <div>
          <div className="analytics-title">Affective Analytics</div>
          <div className="analytics-subtitle">Passive Behavioral Monitoring</div>
        </div>
        <span className="badge" style={{ background: emotionStyle.bg, color: emotionStyle.color, border: `1px solid ${emotionStyle.border}` }}>
          <span className="status-dot" style={{ background: emotionStyle.dot }}></span>
          EMOTIONAL STATE: {emotionalState.toUpperCase()}
        </span>
      </div>

      {/* Metrics */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-label">Response Latency (Δt)</div>
          <div className="metric-value">
            {latency >= 1000 ? Math.round(latency) : latency}
            <span className="metric-unit">ms</span>
          </div>
          <div className="metric-bar">
            <div className="metric-bar-fill" style={{ width: `${latencyBarWidth}%`, background: latency > 30000 ? 'var(--red)' : 'var(--accent)' }} />
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-label">Friction Events (f<sub>r</sub>)</div>
          <div className="metric-value">
            {friction}
            <span className="metric-unit">edits</span>
          </div>
          <div className="metric-bar">
            <div className="metric-bar-fill" style={{ width: `${frictionBarWidth}%`, background: friction > 5 ? 'var(--orange)' : 'var(--green)' }} />
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-label">Sentiment Polarity (S<sub>w</sub>)</div>
          <div className="metric-value" style={{ color: sentiment > 0 ? 'var(--green)' : sentiment < 0 ? 'var(--red)' : 'var(--text-primary)' }}>
            {sentiment > 0 ? '+' : ''}{sentiment.toFixed(1)}
          </div>
          <div className="metric-bar">
            <div className="metric-bar-fill" style={{ width: `${sentimentBarWidth}%`, background: sentiment > 0 ? 'var(--green)' : sentiment < -0.3 ? 'var(--red)' : 'var(--orange)' }} />
          </div>
        </div>
      </div>

      {/* Focus Density */}
      <div className="focus-section">
        <div className="focus-header">
          <span className="focus-label">Focus Density</span>
          <span className="focus-value">{focusDensity}% OPTIMAL</span>
        </div>
        <div className="focus-bar">
          <div className="focus-bar-fill" style={{ width: `${focusDensity}%` }} />
        </div>
      </div>

      {/* Privacy Badge */}
      <div className="privacy-section">
        <div className="privacy-header">
          <div>
            <span className="badge badge-green" style={{ fontSize: '0.6rem', marginBottom: '6px' }}>
              DPDP 2023 COMPLIANT
            </span>
            <div className="privacy-title" style={{ marginTop: '6px' }}>PRIVACY BY DESIGN</div>
          </div>
          <div className="privacy-check">✓</div>
        </div>
        <div className="privacy-text">
          Our system uses <span style={{ color: 'var(--cyan)', textDecoration: 'underline' }}>Text-Based Behavioral Inference</span>. Zero biometric or camera data is captured, ensuring universal accessibility and full privacy compliance.
        </div>
      </div>

      {/* Interaction counter */}
      {interactionCount > 0 && (
        <div style={{ marginTop: '12px', textAlign: 'center', fontSize: '0.7rem', color: 'var(--text-muted)' }}>
          {interactionCount} interaction{interactionCount !== 1 ? 's' : ''} analyzed • Confidence: {(confidence * 100).toFixed(0)}%
        </div>
      )}
    </div>
  );
}
