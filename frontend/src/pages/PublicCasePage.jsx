import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { ShieldCheck, Scale, Globe, Building2, Calendar, FileText, AlertTriangle, AlertCircle } from 'lucide-react';
import api from '../services/api';
import { useLanguage } from '../context/LanguageContext';
import TranslatedText from '../components/common/TranslatedText';

const PublicCasePage = () => {
  const { caseUid } = useParams();
  const { t } = useLanguage();
  const [caseData, setCaseData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPublicData = async () => {
      try {
        const data = await api.getPublicCase(caseUid);
        setCaseData(data);
      } catch (err) {
        setError("This CasePulse record could not be found or is no longer public.");
      } finally {
        setLoading(false);
      }
    };
    fetchPublicData();
  }, [caseUid]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-[#0F172A] p-8">
        <div className="w-12 h-12 border-4 border-primary/30 border-t-primary rounded-full animate-spin mb-4"></div>
        <p className="text-slate-400 font-medium">Fetching verified judgment record...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#0F172A] flex flex-col items-center justify-center p-8">
        <div className="bg-red-500/10 border border-red-500/20 p-12 rounded-3xl text-center max-w-xl shadow-2xl">
          <AlertCircle size={64} className="text-red-500 mx-auto mb-6" />
          <h1 className="text-3xl font-bold text-white mb-4">Record Not Found</h1>
          <p className="text-red-200/60 text-lg leading-relaxed">{error}</p>
          <div className="mt-10 pt-8 border-t border-red-500/10">
            <p className="text-slate-500 text-sm italic font-medium">CasePulse Verification Portal | Government of India</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0F172A] p-4 md:p-12 font-sans">
      <div className="max-w-4xl mx-auto">
        {/* Branding Header */}
        <div className="flex items-center justify-between mb-10">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary/20 rounded-xl">
              <Scale className="text-primary w-8 h-8" />
            </div>
            <div>
              <h1 className="text-2xl font-black text-white tracking-tighter">CasePulse</h1>
              <p className="text-[10px] text-slate-500 font-bold uppercase tracking-[0.2em]">Judicial Action Intelligence</p>
            </div>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-green-500/10 border border-green-500/20 rounded-full text-green-500 text-xs font-black uppercase tracking-widest shadow-lg shadow-green-500/5">
            <ShieldCheck size={16} /> {t("verified")}
          </div>
        </div>

        {/* Hero Summary */}
        <div className="bg-white rounded-[40px] p-8 md:p-12 shadow-2xl mb-8 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-slate-50 rounded-full -mr-32 -mt-32 -z-0"></div>
          
          <div className="relative z-10 space-y-8">
            <div className="space-y-2">
              <p className="text-primary font-black tracking-[0.3em] text-xs uppercase mb-2"><TranslatedText text="Judgment Summary" /></p>
              <h2 className="text-4xl font-bold text-slate-900 leading-tight">
                {caseData.case_title}
              </h2>
              <div className="flex items-center gap-4 text-slate-400 text-sm font-medium pt-2">
                <span>{caseData.case_uid}</span>
                <span className="w-1.5 h-1.5 bg-slate-200 rounded-full"></span>
                <span><TranslatedText text={caseData.case_type} /></span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 py-8 border-y border-slate-100">
              <PublicMeta icon={Building2} label={t("courtName")} value={<TranslatedText text={caseData.court_name} />} />
              <PublicMeta icon={Calendar} label={t("dateOfOrder")} value={<TranslatedText text={caseData.judgment_date} />} />
              <PublicMeta icon={FileText} label={t("department")} value={<TranslatedText text={caseData.related_department} />} />
              <PublicMeta icon={Globe} label="Portal Status" value={t("verified")} color="text-green-600" />
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <div className="w-1.5 h-6 bg-primary rounded-full"></div>
                <TranslatedText text="Executive Summary" />
              </h3>
              <p className="text-slate-600 text-xl leading-relaxed font-serif italic">
                "<TranslatedText text={caseData.summary_text} />"
              </p>
            </div>
          </div>
        </div>

        {/* Public Action Details */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          <ActionCard 
            title={<TranslatedText text="Direction Overview" />} 
            content={<TranslatedText text={caseData.required_action} />} 
            type={<TranslatedText text={caseData.action_type} />}
          />
          <ActionCard 
            title={<TranslatedText text="Compliance Target" />} 
            content={<TranslatedText text={`Department is directed to complete this action within ${caseData.deadline}.`} />}
            priority={caseData.priority}
            risk={caseData.risk_level}
          />
        </div>

        {/* Footer */}
        <div className="text-center space-y-6 pt-12 border-t border-white/5">
          <div className="flex justify-center gap-8 opacity-40">
            <p className="text-white text-[10px] font-bold uppercase tracking-widest">Government of India</p>
            <p className="text-white text-[10px] font-bold uppercase tracking-widest">Judicial Monitoring System</p>
            <p className="text-white text-[10px] font-bold uppercase tracking-widest">Dept of Justice</p>
          </div>
          <p className="text-slate-500 text-xs">
            This information is a verified summary of the official judgment. For legal proceedings, always refer to the certified copy issued by the court.
          </p>
        </div>
      </div>
    </div>
  );
};

const PublicMeta = ({ icon: Icon, label, value, color = "text-slate-900" }) => (
  <div className="flex gap-4">
    <div className="p-3 bg-slate-50 rounded-2xl text-slate-400">
      <Icon size={24} />
    </div>
    <div>
      <p className="text-slate-400 text-[10px] font-black uppercase tracking-widest mb-1">{label}</p>
      <p className={`font-bold text-lg ${color}`}>{value}</p>
    </div>
  </div>
);

const ActionCard = ({ title, content, type, priority, risk }) => (
  <div className="bg-white/5 border border-white/10 p-8 rounded-[32px] backdrop-blur-sm">
    <h4 className="text-white font-bold mb-4 flex items-center justify-between">
      {title}
      {type && <span className="text-[10px] px-2 py-1 bg-primary/20 text-primary rounded-lg uppercase tracking-widest">{type}</span>}
    </h4>
    <p className="text-slate-400 text-sm leading-relaxed mb-6">{content}</p>
    {(priority || risk) && (
      <div className="flex gap-3">
        <span className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase ${priority === 'High' ? 'bg-red-500/10 text-red-500 border border-red-500/20' : 'bg-blue-500/10 text-blue-500 border border-blue-500/20'}`}>
          Priority: {priority}
        </span>
        <span className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase ${risk === 'High' ? 'bg-red-500/10 text-red-500 border border-red-500/20' : 'bg-slate-500/10 text-slate-500 border border-slate-500/20'}`}>
          Risk: {risk}
        </span>
      </div>
    )}
  </div>
);

export default PublicCasePage;
