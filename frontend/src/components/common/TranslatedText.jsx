import React, { useState, useEffect } from 'react';
import { useLanguage } from '../../context/LanguageContext';

const TranslatedText = ({ text, className = "" }) => {
  const { translateDynamicText, selectedLanguage } = useLanguage();
  const [translated, setTranslated] = useState(text);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let isMounted = true;

    const translate = async () => {
      if (!text) {
        setTranslated("");
        return;
      }

      if (selectedLanguage.apiCode === 'en') {
        setTranslated(text);
        return;
      }

      setLoading(true);
      try {
        const result = await translateDynamicText(text);
        if (isMounted) {
          setTranslated(result);
        }
      } catch (error) {
        console.error("Translation error:", error);
        if (isMounted) {
          setTranslated(text);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    translate();

    return () => {
      isMounted = false;
    };
  }, [text, selectedLanguage, translateDynamicText]);

  return (
    <span className={`${className} ${loading ? 'opacity-50 transition-opacity' : ''}`}>
      {translated}
    </span>
  );
};

export default TranslatedText;
