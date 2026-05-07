import React from "react";
import { useLanguage } from "../../context/LanguageContext";
import TranslatedText from "../common/TranslatedText";
import AudioReaderButton from "../common/AudioReaderButton";

export default function ActionPlan({ plan }) {
  const { t } = useLanguage();

  return (
    <div className="bg-surface border border-slate-700 rounded-2xl p-6 shadow-lg">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-bold text-white">{t("actionPlan")}</h3>
        {plan && <AudioReaderButton text={plan} />}
      </div>
      
      {plan ? (
        <div className="space-y-4">
          <div className="p-4 bg-slate-900/50 rounded-xl border border-slate-800 text-slate-200">
            <TranslatedText text={plan} />
          </div>
        </div>
      ) : (
        <p className="text-slate-400 italic">No action plan available.</p>
      )}
    </div>
  );
}
