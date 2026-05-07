import React, { createContext, useContext, useState, useEffect, useCallback, useMemo } from 'react';
import { translations } from '../i18n/translations';
import { translateText as translateApi } from '../services/api';

const LanguageContext = createContext();

export const languageOptions = [
  { code: "en-GB", apiCode: "en", label: "English", native: "English", flag: "GB" },
  { code: "hi-IN", apiCode: "hi", label: "Hindi", native: "हिन्दी", flag: "IN" },
  { code: "ta-IN", apiCode: "ta", label: "Tamil", native: "தமிழ்", flag: "IN" },
  { code: "kn-IN", apiCode: "kn", label: "Kannada", native: "ಕನ್ನಡ", flag: "IN" },
  { code: "te-IN", apiCode: "te", label: "Telugu", native: "తెలుగు", flag: "IN" },
  { code: "ml-IN", apiCode: "ml", label: "Malayalam", native: "മലയാളം", flag: "IN" },
  { code: "mr-IN", apiCode: "mr", label: "Marathi", native: "मराठी", flag: "IN" },
  { code: "gu-IN", apiCode: "gu", label: "Gujarati", native: "ગુજરાતી", flag: "IN" },
  { code: "bn-IN", apiCode: "bn", label: "Bengali", native: "বাংলা", flag: "IN" },
  { code: "pa-IN", apiCode: "pa", label: "Punjabi", native: "ਪੰਜਾਬੀ", flag: "IN" },
  { code: "ur-PK", apiCode: "ur", label: "Urdu", native: "اردو", flag: "PK" },
  { code: "or-IN", apiCode: "or", label: "Odia", native: "ଓଡ଼ିଆ", flag: "IN" }
];

export const LanguageProvider = ({ children }) => {
  const [selectedLanguage, setSelectedLanguageState] = useState(() => {
    const saved = localStorage.getItem("casepulse_language");
    if (saved) {
      const found = languageOptions.find(l => l.code === saved);
      if (found) return found;
    }
    return languageOptions[0]; // English fallback
  });

  const [isSpeaking, setIsSpeaking] = useState(false);

  const stopSpeaking = useCallback(() => {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    setIsSpeaking(false);
  }, []);

  const setSelectedLanguage = useCallback((lang) => {
    stopSpeaking();
    setSelectedLanguageState(lang);
    localStorage.setItem("casepulse_language", lang.code);
  }, [stopSpeaking]);

  const t = useCallback((key) => {
    const langCode = selectedLanguage.code;
    const dictionary = translations[langCode] || translations["en-GB"];
    return dictionary[key] || translations["en-GB"][key] || key;
  }, [selectedLanguage.code]);

  const translateDynamicText = useCallback(async (text) => {
    if (!text || selectedLanguage.apiCode === "en") return text;
    try {
      const translated = await translateApi(text, selectedLanguage.apiCode);
      return translated || text;
    } catch (error) {
      console.error("Translation failed:", error);
      return text;
    }
  }, [selectedLanguage.apiCode]);

  const speakText = useCallback((text) => {
    if (!window.speechSynthesis) {
      console.warn("Speech synthesis not supported in this browser.");
      return;
    }

    stopSpeaking();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = selectedLanguage.code;

    // Try to find a matching voice
    const voices = window.speechSynthesis.getVoices();
    const voice = voices.find(v => v.lang.startsWith(selectedLanguage.apiCode));
    if (voice) {
      utterance.voice = voice;
    }

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  }, [selectedLanguage.code, selectedLanguage.apiCode, stopSpeaking]);

  const value = useMemo(() => ({
    selectedLanguage,
    setSelectedLanguage,
    t,
    translateDynamicText,
    speakText,
    stopSpeaking,
    isSpeaking,
    languageOptions
  }), [selectedLanguage, setSelectedLanguage, t, translateDynamicText, speakText, stopSpeaking, isSpeaking]);

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error("useLanguage must be used within a LanguageProvider");
  }
  return context;
};
