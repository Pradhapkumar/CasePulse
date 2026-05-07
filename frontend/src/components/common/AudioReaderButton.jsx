import React from 'react';
import { useLanguage } from '../../context/LanguageContext';
import { Play, Square } from 'lucide-react';

const AudioReaderButton = ({ text, label }) => {
  const { speakText, stopSpeaking, isSpeaking, t } = useLanguage();

  const handleToggle = () => {
    if (isSpeaking) {
      stopSpeaking();
    } else {
      speakText(text);
    }
  };

  return (
    <button
      onClick={handleToggle}
      className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
        isSpeaking 
          ? 'bg-red-100 text-red-600 hover:bg-red-200' 
          : 'bg-primary/10 text-primary hover:bg-primary/20'
      }`}
      title={isSpeaking ? t("stopAudio") : t("playAudio")}
    >
      {isSpeaking ? (
        <>
          <Square size={18} fill="currentColor" />
          <span>{label || t("stopAudio")}</span>
        </>
      ) : (
        <>
          <Play size={18} fill="currentColor" />
          <span>{label || t("playAudio")}</span>
        </>
      )}
    </button>
  );
};

export default AudioReaderButton;
