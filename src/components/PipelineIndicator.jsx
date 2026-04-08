export default function PipelineIndicator({ activeStage }) {
  const stages = [
    { num: '01', label: 'Signal Extraction' },
    { num: '02', label: 'Ensemble Classification' },
    { num: '03', label: 'RL Adaptation' },
  ];

  return (
    <div className="pipeline">
      {stages.map((stage, i) => {
        const stageNum = i + 1;
        const isActive = activeStage === stageNum;
        const isCompleted = activeStage > stageNum;
        
        return (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div className={`pipeline-stage ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}>
              <span className="pipeline-num">{stage.num}</span>
              {stage.label}
            </div>
            {i < stages.length - 1 && <span className="pipeline-arrow">→</span>}
          </div>
        );
      })}
    </div>
  );
}
