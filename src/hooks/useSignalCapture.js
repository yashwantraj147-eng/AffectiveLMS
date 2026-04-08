import { useState, useRef, useCallback } from 'react';

/**
 * Core behavioural signal capture hook.
 * Captures: response delay, re-edit frequency, raw text, keystroke timing.
 */
export default function useSignalCapture() {
  const [metrics, setMetrics] = useState({
    responseDelay: 0,
    reeditCount: 0,
    rawText: '',
    keystrokeCount: 0,
  });

  const questionShownAt = useRef(Date.now());
  const firstKeystrokeAt = useRef(null);
  const reeditCounter = useRef(0);
  const keystrokeCounter = useRef(0);

  const resetForNewQuestion = useCallback(() => {
    questionShownAt.current = Date.now();
    firstKeystrokeAt.current = null;
    reeditCounter.current = 0;
    keystrokeCounter.current = 0;
    setMetrics({ responseDelay: 0, reeditCount: 0, rawText: '', keystrokeCount: 0 });
  }, []);

  const handleKeyDown = useCallback((e) => {
    // Track first keystroke for response delay
    if (!firstKeystrokeAt.current) {
      firstKeystrokeAt.current = Date.now();
    }

    keystrokeCounter.current += 1;

    // Track re-edits (backspace, delete, cut)
    if (e.key === 'Backspace' || e.key === 'Delete') {
      reeditCounter.current += 1;
    }
    if ((e.ctrlKey || e.metaKey) && (e.key === 'x' || e.key === 'z')) {
      reeditCounter.current += 1;
    }
  }, []);

  const handleTextChange = useCallback((text) => {
    const delay = firstKeystrokeAt.current
      ? firstKeystrokeAt.current - questionShownAt.current
      : Date.now() - questionShownAt.current;

    setMetrics({
      responseDelay: delay,
      reeditCount: reeditCounter.current,
      rawText: text,
      keystrokeCount: keystrokeCounter.current,
    });
  }, []);

  const getSignalPayload = useCallback((sessionId, expectedWords = 20) => {
    const delay = firstKeystrokeAt.current
      ? firstKeystrokeAt.current - questionShownAt.current
      : Date.now() - questionShownAt.current;

    return {
      session_id: sessionId,
      response_delay_ms: delay,
      reedit_count: reeditCounter.current,
      raw_text: metrics.rawText,
      expected_word_count: expectedWords,
      error_type: 'none',
      timestamp: Date.now(),
    };
  }, [metrics.rawText]);

  return {
    metrics,
    handleKeyDown,
    handleTextChange,
    resetForNewQuestion,
    getSignalPayload,
  };
}
