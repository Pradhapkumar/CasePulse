import React from "react";
import { useLanguage } from "../context/LanguageContext";

const LANGUAGES = [
  { code: "en", label: "English", flag: "🇬🇧" },
  { code: "hi", label: "हिन्दी", flag: "🇮🇳" },
  { code: "ta", label: "தமிழ்", flag: "🇮🇳" },
  { code: "kn", label: "ಕನ್ನಡ", flag: "🇮🇳" },
  { code: "te", label: "తెలుగు", flag: "🇮🇳" },
  { code: "ml", label: "മലയാളം", flag: "🇮🇳" },
  { code: "mr", label: "मराठी", flag: "🇮🇳" },
  { code: "gu", label: "ગુજરાતી", flag: "🇮🇳" },
  { code: "bn", label: "বাংলা", flag: "🇮🇳" },
  { code: "pa", label: "ਪੰਜਾਬੀ", flag: "🇮🇳" },
  { code: "ur", label: "اردو", flag: "🇵🇰" },
  { code: "or", label: "ଓଡ଼ିଆ", flag: "🇮🇳" },
];

const LanguageSelector = () => {
  const { language, setLanguage } = useLanguage();

  return (
    <div className="language-selector-wrapper">
      <span className="language-selector-icon">🌐</span>
      <select
        id="language-selector"
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        className="language-selector"
        aria-label="Select language"
      >
        {LANGUAGES.map(({ code, label, flag }) => (
          <option key={code} value={code}>
            {flag} {label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageSelector;
