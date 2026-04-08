const ICONS = {
  simplify: '🔻',
  revisit: '🔄',
  escalate: '🚀',
  switch_modality: '🔀',
};

const TITLES = {
  simplify: 'COGNITIVE SUPPORT ACTIVE',
  revisit: 'PREREQUISITE REVIEW INITIATED',
  escalate: 'CHALLENGE MODE ENGAGED',
  switch_modality: 'MODALITY ADAPTATION',
};

export default function CognitiveAlert({ alert, onDismiss }) {
  if (!alert) return null;

  const icon = ICONS[alert.type] || '⚡';
  const title = TITLES[alert.type] || 'ADAPTATION IN PROGRESS';

  return (
    <div className={`cognitive-alert alert-${alert.type}`}>
      <span className="alert-icon">{icon}</span>
      <div className="alert-content">
        <div className="alert-title">{title}</div>
        <div className="alert-reason">{alert.reason}</div>
      </div>
      <button className="alert-dismiss" onClick={onDismiss}>Dismiss</button>
    </div>
  );
}
