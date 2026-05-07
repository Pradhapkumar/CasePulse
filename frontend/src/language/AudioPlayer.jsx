import React from "react";
import { useLanguage } from "../context/LanguageContext";
import { t } from "../language/translations";

/**
 * AudioPlayer — uses the Web Speech API to read text aloud
 * in the currently selected language (no backend needed).
 *
 * Props:
 *   text     {string}  - The text to speak
 *   language {string}  - Optional override; defaults to global language
 */
const AudioPlayer = ({ text, language: langOverride }) => {
  const { language } = useLanguage();
  const activeLang = langOverride || language;

  const speak = () => {
    if (!text) return;
    window.speechSynthesis.cancel(); // stop any ongoing speech first
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = activeLang;
    window.speechSynthesis.speak(utterance);
  };

  return (
    <button
      id="audio-player-btn"
      onClick={speak}
      className="audio-player-btn"
      aria-label="Read aloud"
      title="Read aloud"
    >
      {t(activeLang, "speak")}
    </button>
  );
};

export default AudioPlayer;
