import { useState } from 'react';
import { DIFFICULTY_COLORS } from '../utils/constants';

export default function ContentCard({ content, topicTitle, difficulty, modality }) {
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [quizIndex, setQuizIndex] = useState(0);

  if (!content) {
    return (
      <div className="content-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '200px', color: 'var(--text-muted)' }}>
          Loading content...
        </div>
      </div>
    );
  }

  const allContent = content.all_content || {};
  const diffColor = DIFFICULTY_COLORS[difficulty] || 'var(--accent)';

  const renderText = () => (
    <div className="content-body">{allContent.text || 'No content available.'}</div>
  );

  const renderVideo = () => {
    const videoUrl = allContent.video || '';
    const embedUrl = videoUrl.replace('watch?v=', 'embed/');
    return (
      <div>
        <iframe
          className="content-video"
          src={embedUrl}
          title={topicTitle}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        />
        <div style={{ marginTop: '12px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
          Video tutorial for {topicTitle} ({difficulty} level)
        </div>
      </div>
    );
  };

  const renderQuiz = () => {
    const quiz = allContent.quiz || [];
    if (quiz.length === 0) return <div className="content-body">No quiz available for this level.</div>;
    
    const q = quiz[quizIndex % quiz.length];
    return (
      <div>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
          Question {quizIndex + 1} of {quiz.length}
        </div>
        <div style={{ fontSize: '1.05rem', fontWeight: 600, marginBottom: '16px', color: 'var(--text-primary)' }}>
          {q.question}
        </div>
        {q.options.map((opt, i) => (
          <button
            key={i}
            className={`quiz-option ${selectedAnswer === i ? (i === q.answer ? 'correct' : 'wrong') : ''}`}
            onClick={() => {
              setSelectedAnswer(i);
              if (i === q.answer) {
                setTimeout(() => {
                  setSelectedAnswer(null);
                  setQuizIndex((prev) => prev + 1);
                }, 1200);
              }
            }}
            disabled={selectedAnswer !== null}
          >
            <span style={{ fontWeight: 600, marginRight: '8px', color: 'var(--accent-light)' }}>
              {String.fromCharCode(65 + i)}.
            </span>
            {opt}
          </button>
        ))}
        {selectedAnswer !== null && selectedAnswer === q.answer && (
          <div style={{ marginTop: '12px', color: 'var(--green)', fontSize: '0.9rem', fontWeight: 600 }}>
            ✓ Correct! Moving to next question...
          </div>
        )}
        {selectedAnswer !== null && selectedAnswer !== q.answer && (
          <div style={{ marginTop: '12px', color: 'var(--red)', fontSize: '0.9rem', fontWeight: 600 }}>
            ✗ Incorrect. The correct answer was {String.fromCharCode(65 + q.answer)}.
            <button
              style={{ marginLeft: '12px', padding: '4px 12px', background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: '6px', color: 'var(--text-primary)', cursor: 'pointer', fontSize: '0.8rem' }}
              onClick={() => { setSelectedAnswer(null); setQuizIndex((prev) => prev + 1); }}
            >Next →</button>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="content-card">
      <div className="content-header">
        <div className="content-title">{topicTitle}</div>
        <span className="badge" style={{ background: `${diffColor}22`, color: diffColor, border: `1px solid ${diffColor}55` }}>
          {difficulty.toUpperCase()}
        </span>
      </div>
      {modality === 'video' ? renderVideo() : modality === 'quiz' ? renderQuiz() : renderText()}
    </div>
  );
}
