import React, { useState } from 'react';
import { Volume2, VolumeX, Loader2 } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

const AudioSummary = ({ text, title }) => {
  const { language } = useLanguage();
  const [isPlaying, setIsPlaying] = useState(false);

  const toggleSpeech = () => {
    if (!('speechSynthesis' in window)) {
      alert("Your browser does not support text to speech!");
      return;
    }

    if (isPlaying) {
      window.speechSynthesis.cancel();
      setIsPlaying(false);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    
    // In a real app, map our language codes to browser BCP 47 tags
    // e.g. 'ta' -> 'ta-IN', 'hi' -> 'hi-IN'
    const langMap = {
      'en': 'en-US',
      'hi': 'hi-IN',
      'ta': 'ta-IN',
      // ... Add others
    };
    
    utterance.lang = langMap[language] || 'en-US';
    
    utterance.onend = () => setIsPlaying(false);
    utterance.onerror = () => setIsPlaying(false);
    
    setIsPlaying(true);
    window.speechSynthesis.speak(utterance);
  };

  // Cleanup on unmount
  React.useEffect(() => {
    return () => {
      window.speechSynthesis.cancel();
    };
  }, []);

  return (
    <button
      onClick={toggleSpeech}
      className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors border ${
        isPlaying 
          ? 'bg-primary/20 text-primary border-primary/50 shadow-[0_0_15px_rgba(59,130,246,0.2)]' 
          : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700 hover:text-white'
      }`}
      title={title || "Listen to summary"}
    >
      {isPlaying ? (
        <>
          <VolumeX className="w-4 h-4 animate-pulse" /> Stop Audio
        </>
      ) : (
        <>
          <Volume2 className="w-4 h-4" /> Listen
        </>
      )}
    </button>
  );
};

export default AudioSummary;
