import { useState, useEffect, useCallback, useRef } from 'react';
import Header from './components/Header';
import InputPanel from './components/InputPanel';
import ContentCard from './components/ContentCard';
import AnalyticsPanel from './components/AnalyticsPanel';
import PipelineIndicator from './components/PipelineIndicator';
import CognitiveAlert from './components/CognitiveAlert';
import useSignalCapture from './hooks/useSignalCapture';
import { sendSignal, getAdaptation, getContent } from './utils/api';
import './App.css';

const SESSION_ID = 'session_' + Date.now();

export default function App() {
  const [emotionalState, setEmotionalState] = useState('Engaged');
  const [confidence, setConfidence] = useState(0);
  const [focusDensity, setFocusDensity] = useState(0);
  const [interactionCount, setInteractionCount] = useState(0);
  const [serverMetrics, setServerMetrics] = useState({
    response_latency: 0, friction_events: 0, sentiment_polarity: 0.0,
  });
  const [currentTopic, setCurrentTopic] = useState('intro-ai');
  const [currentDifficulty, setCurrentDifficulty] = useState('foundational');
  const [currentModality, setCurrentModality] = useState('text');
  const [content, setContent] = useState(null);
  const [topicTitle, setTopicTitle] = useState('Introduction to Artificial Intelligence');
  const [alert, setAlert] = useState(null);
  const [pipelineStage, setPipelineStage] = useState(0);
  const [signalLink, setSignalLink] = useState('IDLE');
  const [isProcessing, setIsProcessing] = useState(false);

  const prevState = useRef('Engaged');
  const { metrics, handleKeyDown, handleTextChange, resetForNewQuestion, getSignalPayload } = useSignalCapture();

  // Load initial content
  useEffect(() => {
    loadContent(currentTopic, currentDifficulty, currentModality);
  }, []);

  const loadContent = async (topic, diff, mod) => {
    try {
      const data = await getContent(topic, diff, mod);
      setContent(data);
      setTopicTitle(data.topic_title);
      resetForNewQuestion();
    } catch (e) {
      console.error('Failed to load content:', e);
    }
  };

  const handleSubmit = useCallback(async () => {
    if (isProcessing) return;
    setIsProcessing(true);
    setSignalLink('TRANSMITTING');

    try {
      // Stage 1: Signal Extraction
      setPipelineStage(1);
      const payload = getSignalPayload(SESSION_ID, 20);
      
      // Stage 2: Classification
      setPipelineStage(2);
      const result = await sendSignal(payload);
      
      setEmotionalState(result.emotional_state);
      setConfidence(result.confidence);
      setFocusDensity(result.focus_density);
      setInteractionCount(result.interaction_count);
      setServerMetrics(result.metrics);
      setSignalLink('SYNCHRONIZED');

      // Check if state changed — trigger adaptation
      if (result.emotional_state !== 'Engaged' && result.emotional_state !== 'Flow-state') {
        // Stage 3: RL Adaptation
        setPipelineStage(3);
        
        const adaptation = await getAdaptation({
          session_id: SESSION_ID,
          current_topic: currentTopic,
          current_difficulty: currentDifficulty,
          current_modality: currentModality,
        });

        if (adaptation.action_type !== 'maintain') {
          setAlert({
            type: adaptation.action_type,
            reason: adaptation.reason,
            from: { topic: currentTopic, difficulty: currentDifficulty, modality: currentModality },
            to: { topic: adaptation.topic, difficulty: adaptation.difficulty, modality: adaptation.modality },
          });

          setCurrentTopic(adaptation.topic);
          setCurrentDifficulty(adaptation.difficulty);
          setCurrentModality(adaptation.modality);
          setTopicTitle(adaptation.topic_title);

          await loadContent(adaptation.topic, adaptation.difficulty, adaptation.modality);
        }
      } else if (result.emotional_state === 'Flow-state') {
        setPipelineStage(3);
        const adaptation = await getAdaptation({
          session_id: SESSION_ID,
          current_topic: currentTopic,
          current_difficulty: currentDifficulty,
          current_modality: currentModality,
        });
        if (adaptation.action_type !== 'maintain') {
          setAlert({
            type: 'escalate',
            reason: adaptation.reason,
            from: { topic: currentTopic, difficulty: currentDifficulty, modality: currentModality },
            to: { topic: adaptation.topic, difficulty: adaptation.difficulty, modality: adaptation.modality },
          });
          setCurrentTopic(adaptation.topic);
          setCurrentDifficulty(adaptation.difficulty);
          setCurrentModality(adaptation.modality);
          setTopicTitle(adaptation.topic_title);
          await loadContent(adaptation.topic, adaptation.difficulty, adaptation.modality);
        }
      }

      prevState.current = result.emotional_state;
      
      setTimeout(() => setPipelineStage(0), 2000);
      setTimeout(() => setSignalLink('SYNCHRONIZED'), 500);
    } catch (e) {
      console.error('Signal submission failed:', e);
      setSignalLink('ERROR');
    } finally {
      setIsProcessing(false);
    }
  }, [currentTopic, currentDifficulty, currentModality, getSignalPayload, isProcessing]);

  const dismissAlert = () => setAlert(null);

  return (
    <div className="app">
      <Header signalLink={signalLink} />
      
      {alert && <CognitiveAlert alert={alert} onDismiss={dismissAlert} />}
      
      <main className="app-main">
        <div className="left-panel">
          <div className="content-meta">
            <div className="meta-badges">
              <span className="badge badge-blue">
                <span className="status-dot" style={{ background: 'var(--accent)' }}></span>
                INPUT MODALITY: TEXTUAL
              </span>
              <span className="badge badge-green">
                PRIVACY: BIOMETRIC-FREE
              </span>
            </div>
            <div className="meta-badges" style={{ marginTop: '6px' }}>
              <span className="badge badge-purple">
                TARGET DIFFICULTY: {currentDifficulty.toUpperCase()}
              </span>
              <span className="badge badge-blue">
                MODALITY: {currentModality.toUpperCase()}
              </span>
            </div>
          </div>

          <ContentCard
            content={content}
            topicTitle={topicTitle}
            difficulty={currentDifficulty}
            modality={currentModality}
          />

          <InputPanel
            onKeyDown={handleKeyDown}
            onTextChange={handleTextChange}
            onSubmit={handleSubmit}
            isProcessing={isProcessing}
            metrics={metrics}
          />

          <div className="signal-status">
            <span style={{ color: 'var(--text-muted)', fontSize: '0.7rem', letterSpacing: '0.1em' }}>
              SIGNAL LINK: <span style={{ color: signalLink === 'SYNCHRONIZED' ? 'var(--green)' : signalLink === 'TRANSMITTING' ? 'var(--orange)' : 'var(--text-muted)' }}>{signalLink}</span>
            </span>
          </div>
        </div>

        <div className="right-panel">
          <AnalyticsPanel
            emotionalState={emotionalState}
            confidence={confidence}
            metrics={serverMetrics}
            focusDensity={focusDensity}
            interactionCount={interactionCount}
            liveMetrics={metrics}
          />
        </div>
      </main>

      <PipelineIndicator activeStage={pipelineStage} />
    </div>
  );
}
