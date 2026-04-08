import { useState } from 'react';

export default function InputPanel({ onKeyDown, onTextChange, onSubmit, isProcessing, metrics }) {
  const [text, setText] = useState('');

  const handleChange = (e) => {
    setText(e.target.value);
    onTextChange(e.target.value);
  };

  const handleSubmit = () => {
    if (text.trim()) {
      onSubmit();
      setText('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="input-panel">
      <textarea
        className="input-area"
        placeholder="Begin typing to generate your learning path..."
        value={text}
        onChange={handleChange}
        onKeyDown={(e) => { onKeyDown(e); handleKeyPress(e); }}
        disabled={isProcessing}
      />
      <div className="input-footer">
        <div className="input-stats">
          <span>Δt: {metrics.responseDelay}ms</span>
          <span>Re-edits: {metrics.reeditCount}</span>
          <span>Words: {metrics.rawText.split(/\s+/).filter(Boolean).length}</span>
        </div>
        <button className="submit-btn" onClick={handleSubmit} disabled={isProcessing || !text.trim()}>
          {isProcessing ? '⟳ Processing...' : '▶ Submit Response'}
        </button>
      </div>
    </div>
  );
}
