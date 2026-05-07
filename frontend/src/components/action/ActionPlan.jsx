import React, { useEffect, useState } from "react";
import { useLanguage } from "../../context/LanguageContext";
import { translateText } from "../../language/translateService";
import { t } from "../../language/translations";
import AudioPlayer from "../../language/AudioPlayer";
import DualView from "../../language/DualView";

export default function ActionPlan({ plan }) {
  const { language } = useLanguage();
  const [translated, setTranslated] = useState(plan);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!plan) return;
    if (language === "en") {
      setTranslated(plan);
      return;
    }
    setLoading(true);
    translateText(plan, language)
      .then(setTranslated)
      .finally(() => setLoading(false));
  }, [language, plan]);

  return (
    <div className="action-plan">
      <h2>{t(language, "actionPlan")}</h2>
      {plan ? (
        <>
          <DualView text={plan} />
          <AudioPlayer text={translated} />
        </>
      ) : (
        <p>{t(language, "noActionPlan")}</p>
      )}
      {loading && <span className="translating-badge">Translating…</span>}
    </div>
  );
}
