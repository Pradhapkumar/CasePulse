import React from 'react';
import { Scale, ShieldCheck, AlertCircle, Info } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import TranslatedText from '../common/TranslatedText';

const LegalSectionTable = ({ sections }) => {
  const { t } = useLanguage();

  if (!sections || sections.length === 0) {
    return (
      <div className="bg-slate-800/50 border border-slate-700 rounded-2xl p-8 text-center">
        <Info className="w-12 h-12 text-slate-500 mx-auto mb-4" />
        <p className="text-slate-400 font-medium">No specific legal sections extracted from this judgment.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 mb-2">
        <Scale className="text-primary w-5 h-5" />
        <h3 className="text-lg font-bold text-white uppercase tracking-wider">
          {t("legalSections") || "Legal Section Analyzer"}
        </h3>
      </div>

      <div className="overflow-x-auto rounded-2xl border border-slate-700 bg-surface shadow-xl">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-800/50 text-slate-400 text-xs font-bold uppercase tracking-widest border-b border-slate-700">
              <th className="px-6 py-4">Section / Act</th>
              <th className="px-6 py-4">Offence Title</th>
              <th className="px-6 py-4">Punishment</th>
              <th className="px-6 py-4 text-center">Confidence</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/50">
            {sections.map((section, idx) => (
              <tr key={idx} className="hover:bg-white/5 transition-colors group">
                <td className="px-6 py-5">
                  <div className="flex flex-col">
                    <span className="text-white font-bold text-lg">
                      Section {section.section_number}
                    </span>
                    <span className="text-primary text-xs font-medium uppercase">
                      {section.act_name}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-5">
                  <p className="text-slate-300 font-medium max-w-xs">
                    <TranslatedText text={section.section_title} />
                  </p>
                </td>
                <td className="px-6 py-5">
                  <div className="flex flex-col gap-2">
                    <div className={`flex items-center gap-1.5 text-xs font-bold uppercase ${section.punishment_explicit ? 'text-green-500' : 'text-slate-500'}`}>
                      {section.punishment_explicit ? (
                        <ShieldCheck size={14} />
                      ) : (
                        <AlertCircle size={14} />
                      )}
                      {section.punishment_explicit ? t("explicit") : t("notExplicit")}
                    </div>
                    <p className="text-slate-400 text-sm italic line-clamp-2 hover:line-clamp-none cursor-default transition-all">
                      <TranslatedText text={section.punishment} />
                    </p>
                  </div>
                </td>
                <td className="px-6 py-5 text-center">
                  <div className="inline-flex items-center justify-center w-12 h-12 rounded-full border-2 border-primary/20 text-primary font-bold text-sm">
                    {Math.round(section.confidence_score * 100)}%
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="p-4 bg-primary/10 border border-primary/20 rounded-xl flex gap-3 items-start">
        <Info className="text-primary w-5 h-5 shrink-0 mt-0.5" />
        <p className="text-slate-400 text-xs leading-relaxed">
          <strong>Important:</strong> This extraction is based on AI pattern matching from the judgment text. It is provided for informational purposes and does not constitute legal advice. Always verify with the original PDF source.
        </p>
      </div>
    </div>
  );
};

export default LegalSectionTable;
