import React from 'react';
import { Shield, Calendar, Scale, Users, FileText } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import TranslatedText from './common/TranslatedText';

const ExtractedDataCard = ({ data }) => {
  const { t } = useLanguage();
  if (!data) return null;

  return (
    <div className="bg-surface border border-slate-700 rounded-2xl overflow-hidden shadow-lg">
      <div className="p-4 border-b border-slate-700 bg-slate-800/50 flex justify-between items-center">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
          <FileText className="w-5 h-5 text-primary" />
          {t("caseDetails")}
        </h3>
        <span className="px-3 py-1 bg-success/20 text-success text-xs font-medium rounded-full flex items-center gap-1 border border-success/30">
          <Shield className="w-3 h-3" />
          {t("verified")}
        </span>
      </div>
      
      <div className="p-6 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-1">
            <span className="text-sm text-slate-400 flex items-center gap-2">
              <FileText className="w-4 h-4" /> {t("caseNumber")}
            </span>
            <p className="text-white font-medium">{data.caseNumber || 'N/A'}</p>
          </div>
          
          <div className="space-y-1">
            <span className="text-sm text-slate-400 flex items-center gap-2">
              <Scale className="w-4 h-4" /> {t("courtName")}
            </span>
            <p className="text-white font-medium">
              <TranslatedText text={data.courtName} />
            </p>
          </div>
        </div>

        <div className="space-y-1">
          <span className="text-sm text-slate-400 flex items-center gap-2">
            <Users className="w-4 h-4" /> {t("petitioner")} / {t("respondent")}
          </span>
          <p className="text-white font-medium">
            <TranslatedText text={data.parties} />
          </p>
        </div>

        <div className="space-y-1 p-4 bg-slate-900 rounded-xl border border-slate-800">
          <span className="text-sm text-slate-400 font-medium block mb-2">{t("keyDirections")}</span>
          <div className="text-white text-sm">
            <TranslatedText text={data.keyDirections} />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="space-y-1">
            <span className="text-sm text-slate-400 flex items-center gap-2">
              <Scale className="w-4 h-4" /> {t("caseType")}
            </span>
            <p className="text-white font-medium">
              <TranslatedText text={data.caseType} />
            </p>
          </div>
          <div className="space-y-1">
            <span className="text-sm text-slate-400 flex items-center gap-2">
              <Calendar className="w-4 h-4" /> {t("judgmentDate")}
            </span>
            <p className="text-white font-medium">
              <TranslatedText text={data.judgmentDate} />
            </p>
          </div>
          <div className="space-y-1">
            <span className="text-sm text-slate-400 flex items-center gap-2">
              <FileText className="w-4 h-4" /> {t("hearings")}
            </span>
            <p className="text-white font-medium">
              <TranslatedText text={data.hearingsCount} />
            </p>
          </div>
        </div>

        <div className="space-y-1">
          <span className="text-sm text-slate-400 flex items-center gap-2">
            <Calendar className="w-4 h-4" /> {t("deadline")}
          </span>
          <p className="text-warning font-semibold">
            <TranslatedText text={data.timeline} />
          </p>
        </div>
      </div>
    </div>
  );
};

export default ExtractedDataCard;
