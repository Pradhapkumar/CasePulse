import React, { useEffect, useState } from "react";
import { useLanguage } from "../context/LanguageContext";
import { translateText } from "../language/translateService";

/**
 * DualView — shows English original alongside a live translation.
 * Great for AI-generated content (summaries, action plans, etc.)
 *
 * Props:
 *   text {string} - The original English text
 */
const DualView = ({ text }) => {
  const { language } = useLanguage();
  const [translated, setTranslated] = useState(text);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (language === "en") {
      setTranslated(text);
      return;
    }
    setLoading(true);
    translateText(text, language)
      .then(setTranslated)
      .finally(() => setLoading(false));
  }, [language, text]);

  if (language === "en") {
    return <div className="dual-view-single">{text}</div>;
  }

  return (
    <div className="dual-view-grid">
      <div className="dual-view-panel">
        <h3 className="dual-view-label">English</h3>
        <p>{text}</p>
      </div>
      <div className="dual-view-panel">
        <h3 className="dual-view-label">Translated</h3>
        {loading ? (
          <span className="dual-view-loading">Translating…</span>
        ) : (
          <p>{translated}</p>
        )}
      </div>
    </div>
  );
};

export default DualView;
