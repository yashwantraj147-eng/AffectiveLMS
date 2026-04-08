export default function Header({ signalLink }) {
  return (
    <header className="header">
      <div className="header-brand">
        <div className="header-logo">🧠</div>
        <div>
          <div className="header-title">AFFECTIVE<span>LMS</span></div>
          <div className="header-subtitle">Zero-Hardware Emotion-Aware Framework</div>
        </div>
      </div>
      <div>
        <span className="badge badge-green">
          <span className="status-dot" style={{ background: signalLink === 'SYNCHRONIZED' ? '#10b981' : signalLink === 'TRANSMITTING' ? '#f59e0b' : '#64748b' }}></span>
          NEURAL LINK: {signalLink}
        </span>
      </div>
    </header>
  );
}
